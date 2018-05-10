#-*- coding:utf-8 -*-
import logging
import os
import time

LOG_PATH = os.path.normpath(os.path.dirname(__file__) + time.strftime(
    "\\logs\\%Y-%m-%d.log", time.localtime()))
LOGGING_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] ' \
                 '%(levelname)s %(message)s'
DATA_FORMAT = "%a, %d %b %Y %H:%M:%S"

class Logging:
    """
    日志管理类
    """
    def __init__(self, level = logging.DEBUG, format=LOGGING_FORMAT,
                 datefmt=DATA_FORMAT, filename=LOG_PATH,
                 filemode="w"):
        '''
        :param level: 日志级别
        :param format: 日志格式
        :param datefmt: 日期格式
        :param filename: 日志文件名
        :param filemode: 文件打开模式
        '''
        self.level = level
        self.format = format
        self.datefmt = datefmt
        self.filename = filename
        self.filemode = filemode

        # 初始化日志，同时输出到console和文件
        logging.basicConfig(level=self.level, format=self.format,
                            datefmt=self.datefmt, filename=self.filename,
                            filemode=self.filemode)

        # 定义StreamHandler，将INFO或更高级别的日志信息打印到标准错误
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s'
        )
        console.setFormatter(formatter)
        logging.getLogger('Logger').addHandler(console)
        self.log = logging.getLogger('Logger')

    def output(self, msg, level=logging.DEBUG):
        '''
        日志输出
        :param msg: 输出信息
        :param level: 级别：debug
        :return: 
        '''
        if level == logging.DEBUG:
            # 调试信息
            self.log.debug(msg)
        elif level == logging.INFO:
            # 一般的信息
            self.log.info(msg)
        elif level == logging.WARNING:
            # 警告信息
            self.log.warning(msg)
        elif level == logging.ERROR:
            # 错误信息
            self.log.error(msg)
        else:
            self.log.critical(msg)

    def set_level(self, level=logging.DEBUG):
        self.log.setLevel(level)