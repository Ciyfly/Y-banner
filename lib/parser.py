#!/usr/bin/python
# coding=utf-8
'''
@Author: Recar
@Date: 2020-05-02 19:21:56
@LastEditors: Recar
@LastEditTime: 2020-05-02 19:22:26
'''
from optparse import OptionParser
from config.config import VERSION, BANNER
USAGE = "python main.py -d xxx.com"
import sys


def get_options():
    print(BANNER)
    parser = OptionParser(usage=USAGE,version=VERSION)

    parser.add_option('-d', type=str, dest="domains", help="指定要测试的域名")

    parser.add_option('-f', type=str, dest="domain_file", help="指定域名列表文件")
    
    parser.add_option('--rm', action='store_true', dest="rm_output", default=False, help="清空所有报告")

    (options, args) = parser.parse_args()
    if options.domains == None and options.domain_file == None and options.rm_output == False:
        parser.print_help()
        sys.exit(0)
    if options.domains:
        if "http://" in options.domains or "https://" in options.domains:
            options.domains =options.domains.replace("http://", "").replace("https://", "")
        if "," in options.domains:
            options.domains = options.domains.split(",")
        else:
            options.domains = [options.domains]
    return options