"""MySQL target class."""

from __future__ import annotations
from collections import Counter
import copy

import io
from threading import Lock
import threading
import time
import typing as t
from pathlib import PurePath

import simplejson as json
from prometheus_client import start_http_server
from singer_sdk import typing as th
from singer_sdk.target_base import SQLTarget

from macrometa_target_mysql.constants import (
    export_errors,
    fabric_label,
    region_label,
    registry_package,
    tenant_label,
    workflow_label,
)
from macrometa_target_mysql.sinks import MySQLSink


class MacrometaTargetMySQL(SQLTarget):
    """Sample target for MySQL."""

    name = "macrometa-target-mysql"

    default_sink_class = MySQLSink
    flush_lock = Lock()

    def __init__(
        self,
        *,
        config: dict | PurePath | str | list[PurePath | str] | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        super().__init__(
            config=config,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )

        # Start the Prometheus HTTP server for exposing metrics
        self.logger.info("MySQL target is starting the metrics server.")
        start_http_server(8001, registry=registry_package)

    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL username",
        ),
        th.Property(
            "password",
            th.StringType,
            secret=True,  # Flag config as protected.
            description="MySQL password",
        ),
        th.Property(
            "host",
            th.StringType,
            description="MySQL host",
        ),
        th.Property(
            "port",
            th.IntegerType,
            description="MySQL port",
        ),
        th.Property(
            "database",
            th.StringType,
            description="MySQL database",
        ),
        th.Property(
            "target_table",
            th.StringType,
            description="MySQL table name",
        ),
        th.Property(
            "lower_case_table_names",
            th.BooleanType,
            description="Lower case table names",
            default=True,
        ),
        th.Property(
            "allow_column_alter",
            th.BooleanType,
            description="Allow column alter",
            default=False,
        ),
        th.Property(
            "replace_null",
            th.BooleanType,
            description="Replace null to blank",
            default=False,
        ),
        th.Property(
            "batch_flush_size", th.IntegerType, description="Batch Size", default=False
        ),
        th.Property(
            "batch_flush_interval",
            th.IntegerType,
            description="Batch Flush Interval (Minutes)",
            default=False,
        ),
        th.Property(
            "batch_flush_size", th.IntegerType, description="Batch Size", default=10000
        ),
        th.Property(
            "hard_delete",
            th.BooleanType,
            description="When `hard_delete` option is true, then DELETE SQL commands will be performed "
            "in MySQL to delete rows in tables. It is achieved by continuously checking "
            "the `_SDC_DELETED_AT` metadata column sent by the data source. Due to deleting "
            "rows requires metadata columns, `hard_delete` option automatically enables the"
            " `add_metadata_columns` option as well. Calculation of Metrics such as `exported_bytes`,"
            "will include _SDC_ columns' byte count.",
            default=False,
        ),
        th.Property(
            "add_metadata_columns",
            th.BooleanType,
            description="Metadata columns add extra row level information about data ingestion, "
            "(i.e. when was the row read in source, when was inserted or deleted in "
            "mysql etc.) Metadata columns are created automatically by adding extra "
            "columns to the tables with a column prefix `_SDC_`. The column names are "
            "following the stitch naming conventions documented at "
            "https://www.stitchdata.com/docs/data-structure/integration-schemas#sdc-columns.",
            default=False,
        ),
    ).to_dict()

    schema_properties = {}

    def _process_lines(self, file_input: t.IO[str]) -> t.Counter[str]:
        counter:Counter[str] = None
        flusher = threading.Thread(
            target=self._flush_task, args=[self.config.get("batch_flush_interval")]
        )
        flusher.start()

        if self.config.get("replace_null", False):
            processed_input = io.StringIO()
            for line in file_input:
                data = self.deserialize_json(line.strip())

                if data.get("type", "") == "SCHEMA":
                    self.schema_properties = data["schema"]["properties"]
                elif data.get("type", "") == "RECORD":
                    for key, value in data.get("record", {}).items():
                        if value is not None:
                            continue

                        # https://json-schema.org/understanding-json-schema/reference/type.html
                        _type = self.schema_properties[key]["type"]
                        data_types = _type if isinstance(_type, list) else [_type]

                        if "null" in data_types:
                            continue
                        if "string" in data_types:
                            data["record"][key] = ""
                        elif "object" in data_types:
                            data["record"][key] = {}
                        elif "array" in data_types:
                            data["record"][key] = []
                        elif "boolean" in data_types:
                            data["record"][key] = False
                        else:
                            data["record"][key] = 0

                processed_input.write(json.dumps(data) + "\n")
            processed_input.seek(0)
            try:
                counter = super()._process_lines(processed_input)
            except Exception as e:
                # Increment export_errors metric
                export_errors.labels(
                    region_label, tenant_label, fabric_label, workflow_label
                ).inc()
                raise e
        else:
            try:
                counter = super()._process_lines(file_input)
            except Exception as e:
                # Increment export_errors metric
                export_errors.labels(
                    region_label, tenant_label, fabric_label, workflow_label
                ).inc()
                raise e

        # Process any missed records before exiting
        with self.flush_lock:
            self.drain_all()

        return counter

    def _process_record_message(self, message_dict: dict) -> None:
        """Process a RECORD message.

        Args:
            message_dict: TODO
        """
        self._assert_line_requires(message_dict, requires={"stream", "record"})

        stream_name = message_dict["stream"]
        self._assert_sink_exists(stream_name)

        for stream_map in self.mapper.stream_maps[stream_name]:
            raw_record = copy.copy(message_dict["record"])
            transformed_record = stream_map.transform(raw_record)
            if transformed_record is None:
                # Record was filtered out by the map transform
                continue

            sink = self.get_sink(stream_map.stream_alias, record=transformed_record)
            context = sink._get_context(transformed_record)
            if sink.include_sdc_metadata_properties:
                sink._add_sdc_metadata_to_record(
                    transformed_record,
                    message_dict,
                    context,
                )
            else:
                sink._remove_sdc_metadata_from_record(transformed_record)

            sink._validate_and_parse(transformed_record)
            transformed_record = sink.preprocess_record(transformed_record, context)
            sink._singer_validate_message(transformed_record)

            sink.tally_record_read()
            sink.process_record(transformed_record, context)
            sink._after_process_record(context)

            if sink.is_full:
                self.logger.info(
                    "Target sink for '%s' is full. Draining...",
                    sink.stream_name,
                )
                self.flush_lock.acquire(False)
                self.drain_one(sink)
                self.flush_lock.release()

    def _flush_task(self, interval) -> None:
        while True:
            time.sleep(interval * 60)
            self.logger.debug(
                "Max age %sm reached for the batch. Draining all sinks.",
                interval,
            )
            with self.flush_lock:
                self.drain_all()

    def _handle_max_record_age(self) -> None:
        return


if __name__ == "__main__":
    MacrometaTargetMySQL.cli()
