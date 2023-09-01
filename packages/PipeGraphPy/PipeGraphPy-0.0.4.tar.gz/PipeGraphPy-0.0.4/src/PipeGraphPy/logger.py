#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from PipeGraphPy.config import settings
from PipeGraphPy.db.models import PredictRecordTB, OnlineGraphsPredictRecordTB, RunRecordTB
from rabbitmqpy import LogPuber


def log_dec(level):
    def wrapper(func):
        def _(cls, msg, **extra):
            try:
                f = getattr(cls.logger, level)
                if settings.SDK_SHOW_LOG:
                    print(msg)
                if extra.get("plog_record_id"):
                    plog_record_id = extra.pop("plog_record_id")
                    PredictRecordTB.add_log(id=plog_record_id, msg=msg)
                if extra.get("rlog_record_id"):
                    rlog_record_id = extra.pop("rlog_record_id")
                    RunRecordTB.add_log(id=rlog_record_id, msg=msg)
                if extra.get("online_plog_record_id"):
                    plog_record_id = extra.pop("online_plog_record_id")
                    OnlineGraphsPredictRecordTB.add_log(id=plog_record_id, msg=msg)
                f(msg)
            except:
                pass
        return _
    return wrapper

def mq_logger(filepath):
    exchange = '%s_mqlog' % settings.SAVE_FOLDER
    routing_key = '%s_mqlog_key' % settings.SAVE_FOLDER
    logger = LogPuber(filepath, settings.AMQP_URL, exchange, 'direct', routing_key=routing_key)
    return logger


def get_logger(folder="run"):
    # 不需要mq消息记录日志
    # try:
    #     if not settings.DEBUG and settings.RUN_PERMISSION:
    #         logger = mq_logger("/data/algo/%s/logs/PipeGraphPy/%s/PipeGraphPy_rpc.log" %
    #                 (settings.SAVE_FOLDER, folder))
    #         logger = logging.getLogger("PipeGraphPy")
    #     else:
    #         logger = logging.getLogger("PipeGraphPy")
    # except:
    #     return logging.getLogger("PipeGraphPy")
    # return logger
    return logging.getLogger(folder)


class LogBase(object):
    __function__ = None
    logger = logging.getLogger("PipeGraphPy")

    @classmethod
    @log_dec("info")
    def info(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("error")
    def error(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("warning")
    def warning(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("warn")
    def warn(cls, msg, **extra):
        pass

    @classmethod
    @log_dec("debug")
    def debug(cls, msg, **extra):
        pass


class plog(LogBase):
    """预测使用的log"""

    __function__ = "predict"
    logger = get_logger("predict")

    @classmethod
    def log(cls, level, msg, **kwargs):
        if hasattr(cls, level):
            f = getattr(cls, level)
            extra = {}
            for i in ["graph_id","rlog_record_id", "plog_record_id", "source", "clock"]:
                if kwargs.get(i):
                    extra[i] = kwargs[i]
            f(msg, **extra)


class rlog(LogBase):
    """运行使用的log"""

    __function__ = "run"
    logger = get_logger("run")


class log(LogBase):
    """一般log"""
    __function__ = "rpc"
    logger = get_logger("rpc")

