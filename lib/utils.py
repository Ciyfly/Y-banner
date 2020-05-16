#!/usr/bin/python
# coding=utf-8
'''
@Author: Recar
@Date: 2020-05-02 19:11:42
@LastEditors: Recar
@LastEditTime: 2020-05-02 19:21:49
'''
import os


class Utils(object):
    @staticmethod
    def is_windows():
        if os.name == "nt":
            return True


