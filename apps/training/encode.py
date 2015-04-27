# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2015年4月24日

@author: xu.wang
'''

import codecs
from fileinput import filename
import json
import os

INLINE_STRING = "这是一个String 串"  # 这是一个字节串, 编码格式同当前文件

INLINE_UNICODE = u"这是一个Unicode 串"  # 这是一个unicode 串，编码格式与当前文件无关

FILE_CONFIG = {
    "ansi.csv": "gbk",
    "utf-8-nobom.csv": "utf-8",
    "unicode_be.csv": "utf-16",
    "unicode_le.csv": "utf-16"
}

EXTRA_CONFIG = {
    "extra_ansi.py": "gbk",
    "extra_unicode.py": "utf-16",
    "extra_utf-8.py": "utf-8"
    # "extra_utf-8_bom.py": "utf-8"
}


def get_data_file(file_name):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    file_path = os.path.join(file_path, "data", file_name)

    return file_path


def save_py(file_name, extra):
    if not extra:
        return False
    if not (isinstance(extra, dict) or isinstance(extra, list)):
        return False
    try:
        ss = json.dumps(extra,  ensure_ascii=False,
                        indent=4,
                        encoding="utf-8",
                        sort_keys=True)
        file_name = get_data_file(file_name)
        fs = open(file_name, "w")
        fs.write(ss)
        fs.close()
        return True
    except Exception, ex:
        print "save_py() exception:", ex
        return False


def read_text():
    '''
    @summary: open() 直接读取文件. readline() 内容为字节串，编码同源文件
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
    @summary: codecs.open()读取文件, 需要指定编码,  readline() 是unicode字符串
    '''
    for key in FILE_CONFIG:
        filename = get_data_file(key)
        encoding = FILE_CONFIG[key]
        print "\r\n##File:", filename
        with codecs.open(filename, mode="rb", encoding=encoding,
                         errors="strict", buffering=1) as fs:
            for i in range(0, 5):
                if i == 0:
                    pass
                line = fs.readline()
                print "source:%s, type=%s" % (line, type(line))


def write_json():
    '''
    @summary: 1> 从CSV文件中读取内容;  2>构建为字典; 3 >再将字典序列化成py文件
    '''
    for key in FILE_CONFIG:
        filename = get_data_file(key)
        encoding = FILE_CONFIG[key]
        with codecs.open(filename, "r", encoding=encoding) as fs:
            line = fs.readline()
            row = line.split(",")
            if len(row) > 3:
                extra = {
                    "adcode": row[0].encode("utf-8"),
                    "name": row[1].encode("utf-8"),
                    "package": row[2].encode("utf-8")
                }
                file_name = extra.get("adcode") + FILE_CONFIG[key] + ".py"
                save_py(file_name, extra)


def read_json():
    '''
    @summary: 从文件中load 对象时的编码. 对于utf-8 BOM 要去BOM
    '''
    for key in EXTRA_CONFIG:
        filename = get_data_file(key)
        encoding = EXTRA_CONFIG[key]
        result = False
        try:
            fs = open(filename)
            json.load(fs, encoding=encoding)
            fs.close()
            result = True
        except Exception:
            pass

        if not result:
            try:
                fs = codecs.open(filename, "r", encoding=encoding)
                ss = fs.read()
                fs.close()
                content = ss.encode("utf-8")
                json.loads(content, "utf-8")
                print "Try successfully!"
            except Exception, ex:
                print "Try failed: %s. error:%s" % (filename, ex)
