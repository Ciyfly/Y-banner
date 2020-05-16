#!/usr/bin/python
# coding=UTF-8

import logging
import logging.handlers


def get_logger(
    console=True, log_file=None, level=logging.INFO,
    maxBytes=2*1024, backupCount=5, log_name='banner'
    ):
    # log_name 是用于区分 不然对于同一个log会不断 addHandler
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    formatter = logging.Formatter(
         '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    if log_file:
    # 使用FileHandler输出到文件
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=maxBytes, backupCount=backupCount, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    if console:
        # 使用StreamHandler输出到屏幕
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        # 添加两个Handler
        logger.addHandler(ch)
    return logger

logger = get_logger()
