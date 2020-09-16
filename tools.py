#!/usr/bin/env python  
# -*- coding:utf-8 -*-  
""" 
@author:  wangye
@file: tools.py 
@time: 2020/09/16
@contact: wangye.hope@gmail.com
@site:  
@software: PyCharm 
"""

import os


def list_all_files(root: str, keys=[], outliers=[], full_path=False):
    """
    列出某个文件下所有文件的全路径

    Author:   wangye
    Datetime: 2019/4/16 18:03

    :param root: 根目录
    :param keys: 所有关键字
    :param outliers: 所有排除关键字
    :param full_path: 是否返回全路径，True为全路径
    :return:
            所有根目录下包含关键字的文件全路径
    """
    _files = []
    _list = os.listdir(root)
    for i in range(len(_list)):
        path = os.path.join(root, _list[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path, keys, outliers, full_path))
        if os.path.isfile(path) \
                and all([k in path for k in keys]) \
                and not any([o in path for o in outliers]):
            _files.append(os.path.abspath(path) if full_path else path)
    return _files
