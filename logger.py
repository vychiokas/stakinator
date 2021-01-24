from __future__ import annotations
# from singleton import SingletonMeta
import logging
from logging.handlers import RotatingFileHandler

class SingletonMeta(type):
  _instance = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instance:
      cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
    return cls._instance[cls]

class MyLogger(metaclass=SingletonMeta):
    _5MB = 5*1024*1024
    __instance = None
    _FORMAT = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    _INSTANCE: MyLogger = None

    def __new__(cls, log_name: str, log_file_path: str):
        return super(MyLogger, cls).__new__(cls)

    def __init__(self, log_name: str, log_file_path: str) -> None:
        self._log_name = log_name
        self._log_file_path = log_file_path
        log_formatter = logging.Formatter(MyLogger._FORMAT)
        log_handler = RotatingFileHandler(log_file_path, mode='a',
                                            maxBytes=MyLogger._5MB,
                                            backupCount=2,
                                            encoding="utf-8",
                                            delay=0)
        log_handler.setFormatter(log_formatter)
        log_handler.setLevel(logging.INFO)

        log = logging.getLogger(log_name)
        log.setLevel(logging.INFO)
        log.addHandler(log_handler)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter
        # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(log_formatter)

        # add ch to logger
        log.addHandler(ch)
        self._logger = log

    @property
    def logger(self):
        return self._logger