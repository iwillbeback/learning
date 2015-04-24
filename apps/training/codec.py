# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年4月24日

@author: xu.wang
'''

import codecs
import os
from win32con import FILE_NAME_NORMALIZED


def get_data_file(file_name):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    file_path = os.path.join(file_path, "data", file_name)

    return file_path


def read_text():
    '''
    @summary: 用open(), 直接读取有BOM的utf-8格式文件. readline() 是字节串
    '''
    file_name = get_data_file("utf-8.csv")
    with open(file_name, "r") as fs:
        line = fs.readline()
        print "#line source:%s\r\n type=%s" % (line, type(line))

        line_unicode = line.decode("gbk")  # line.decode("utf-8") 出错
        print "#line unicod:%s\r\n type=%s" % (line_unicode,
                                               type(line_unicode))


def read_codec():
    '''
    @summary: 用codecs.open() 读取utf-8编码的文件. readline() 是unicode 串
    @attention: 对于有BOM 的utf-8编码的文件， 对于第一行文件。需要忽略第1个字符

    '''
    filename = get_data_file("utf-8.csv")
    with codecs.open(filename=filename, mode="r", encoding="utf-8",
                     errors="strict", buffering=1) as fs:
        line = fs.readline()
        # print "source:%s, type=%s" % (line, type(line)) 出异常
        print "source:%s, type=%s" % (line[1:], type(line))

    filename = get_data_file('utf-8-nobom.csv')

    with codecs.open(filename, mode="rb", encoding="utf-8",
                     errors="strict", buffering=1) as fs:
        line = fs.readline()
        print "source:%s, type=%s" % (line, type(line))
