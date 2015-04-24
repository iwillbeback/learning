# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年4月24日

@author: xu.wang
'''

import codecs
import os


def get_data_file(file_name):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    file_path = os.path.join(file_path, "data", file_name)

    return file_path


def read_text():
    '''
    @summary: 用open(), 直接读取有BOM的utf-8格式文件. readline() 是字节串.
    @summary: 且需要去除BOM
    '''
    file_name = get_data_file("utf-8.csv")
    with open(file_name, "r") as fs:
        for i in range(0, 3):
            line = fs.readline()
            if (i == 0) and (line[:3] == codecs.BOM_UTF8):
                '''
                # 去除BOM
                '''
                line = line[3:]
            line_unicode = line.decode("utf-8")
            # print "source:%s, type=%s" % (line, type(line))
            print "decode:%s, type=%s" % (line_unicode, type(line_unicode))


def read_codec():
    '''
    @summary: 用codecs.open()读取文件需要指定编码,  readline() 是unicode字符串

    '''

    extra = {"ansi.csv": "gbk",
             "utf-8-nobom.csv": "utf-8",
             "unicode_be.csv": "utf-16",
             "unicode_le.csv": "utf-16"
             }

    for key in extra:
        filename = get_data_file(key)
        encoding = extra[key]
        print "\r\n##File:", filename
        with codecs.open(filename, mode="rb", encoding=encoding,
                         errors="strict", buffering=1) as fs:
            for i in range(0, 5):
                if i == 0:
                    pass
                line = fs.readline()
                print "source:%s, type=%s" % (line, type(line))
