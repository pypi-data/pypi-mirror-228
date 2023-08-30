import logging
from multiprocessing import Process, Queue
from dataclasses import dataclass


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Logger:
    def __init__(self):
        self._logging_modules: dict[str, LoggingObject] = {}

    def logging(self, name: str, level: str | int, message: str):
        self._logging_modules[name].logging(level=level, message=message)

    def set_logger(self, name: str, level: str | int, handler_def: dict[int, dict], format_def: tuple):
        log_queue = Queue()
        logging_process = LoggingProcess(log_queue=log_queue, name=name, level=level, handler_def=handler_def,
                                         format_def=format_def)
        logging_object = LoggingObject(log_queue=log_queue, logging_process=logging_process)
        self._logging_modules[name] = logging_object
        self._logging_modules[name].start()


class LoggingProcess(Process):
    def __init__(self, log_queue: Queue, name: str, level: str | int, handler_def: dict[int, dict], format_def: tuple):
        super(LoggingProcess, self).__init__()
        logging.basicConfig(level=logging.INFO)
        self._name = name
        self._level = level
        self._handler_def = handler_def
        self._format_str = format_def
        self._log_queue = log_queue
        self._logger = None

    def run(self) -> None:
        from logging import handlers
        logging.basicConfig(level=self._level)
        self._logger = logging.getLogger(self._name)
        self._logger.setLevel(self._level)
        self._logger.propagate = False
        formatter = logging.Formatter(*self._format_str)
        for handler_type, args in self._handler_def.items():
            if handler_type == HandlerType.StreamHandler:
                handler = logging.StreamHandler(**args)
            elif handler_type == HandlerType.TimedRotateFileHandler:
                handler = handlers.TimedRotatingFileHandler(**args)
            else:
                raise Exception("handler type not supported")
            handler.setFormatter(formatter)
            handler.setLevel(self._level)
            self._logger.addHandler(handler)

        while True:
            log_message = self._log_queue.get()
            if log_message.level == logging.INFO:
                self._logger.info(log_message.message)
            elif log_message.level == logging.WARNING:
                self._logger.warning(log_message.message)
            elif log_message.level == logging.ERROR:
                self._logger.error(log_message.message)
            elif log_message.level == logging.DEBUG:
                self._logger.debug(log_message.message)


class LoggingObject:
    def __init__(self, log_queue: Queue, logging_process: LoggingProcess):
        self._log_queue: Queue = log_queue
        self._logging_process: LoggingProcess = logging_process

    def logging(self, level: str | int, message: str):
        self._log_queue.put(LogMessage(level=level, message=message))

    def start(self):
        self._logging_process.start()


class HandlerType:
    StreamHandler = 0
    TimedRotateFileHandler = 1


@dataclass
class LogMessage:
    level: str | int
    message: str

