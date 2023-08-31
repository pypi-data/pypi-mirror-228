from typing import Union, List

import logging
import sys
import time
from pythonjsonlogger import jsonlogger

# root = logging.getLogger()
# root.setLevel(logging.INFO)
#
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.INFO)
# formatter = jsonlogger.JsonFormatter()
# handler.setFormatter(formatter)
# root.addHandler(handler)

class JsonFormatterWithTime(jsonlogger.JsonFormatter):
    def format(self, record):
        if 'msg' in record.__dict__:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            record.__dict__['msg'] = f"{current_time} - {record.__dict__['msg']}"
        return super().format(record)
class OutputLogger:
    handler=None
    print_time=False
    def __init__(self, unique_name, log_level='INFO', print_time=False) -> None:
        self.data = None
        self.host = None
        self.service_account = None
        self.unique_name = unique_name
        self.print_time = print_time

        self.logger = logging.getLogger(unique_name)
        self.logger.propagate = False # Disable propagation to the root logger
        if len(self.logger.handlers):
            self.logger.removeHandler(self.logger.handlers[0])
        if self.handler is None:
            self.handler = logging.StreamHandler(sys.stdout)
            formatter = jsonlogger.JsonFormatter()
            if print_time:
                formatter = JsonFormatterWithTime()
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)
        self.set_log_level(log_level)

    def set_log_level(self, log_level: str) -> None:
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError(f"Invalid log level: {log_level}")

        if self.logger:
            self.logger.setLevel(numeric_level)
        if self.handler and len(self.logger.handlers):
            self.handler.setLevel(numeric_level)

    def save_request_info(self, data, host, service_account) -> None:
        self.data = data
        self.host = host
        self.service_account = service_account

    def log_output(self, output, retrieve_type='', pipeline_timing=None, predictable_object_count=None):

        extra_info = dict(input=self.data, output=output, from_host=self.host,
                          from_service_account=self.service_account,)
        if pipeline_timing:
            extra_info.update({"pipeline_exec_time": pipeline_timing,
                               "predictable_object_count": predictable_object_count})
        self.logger.info(f"INFO {self.unique_name} invoked {retrieve_type}", extra=extra_info)

    def log_output_company(self, output, retrieve_type='', company=None, pipeline_timing=None, predictable_object_count=None):

        extra_info = dict(input=self.data, output=output, from_host=self.host,
                          from_service_account=self.service_account)
        if pipeline_timing:
            extra_info.update({"pipeline_exec_time": pipeline_timing,
                               "predictable_object_count": predictable_object_count})
        if company and 'name' in company:
            extra_info.update({"company": company['name']})
        self.logger.info(f"INFO {self.unique_name} invoked {retrieve_type}", extra=extra_info)

    def log(self, level, message, extra=None):
        if extra is not None:
            if isinstance(extra, str):
                extra = {"message": extra}
            elif isinstance(extra, dict):
                extra = extra.copy()
            else:
                extra = None

        self.logger.log(level, f'{logging.getLevelName(level).upper()} - {self.unique_name} - {message}', extra=extra)

    def debug(self, message, extra=None):
        self.log(logging.DEBUG, message, extra=extra)

    def info(self, message, extra=None):
        self.log(logging.INFO, message, extra=extra)

    def warning(self, message, extra=None):
        self.log(logging.WARNING, message, extra=extra)

    def error(self, message, extra=None):
        self.log(logging.ERROR, message, extra=extra)

    def exception(self, message, extra=None):
        self.log(logging.ERROR, message, extra=extra)