#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 16:46
# @Author  : sgwang
# @File    : file_util.py
# @Software: PyCharm
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
FILES_PATH = os.path.join(ROOT_PATH, 'files')


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
        except FileExistsError:
            pass


def list_dir_file(dir_name):
    dir_path_name = os.path.join(FILES_PATH, dir_name)
    if not os.path.exists(dir_path_name):
        return []
    return os.listdir(dir_path_name)


def merge_all_ts(merge_file_name, prefix_merge_dir, prefix_ts_dir, ts_file_name_list):
    try:
        merge_file = os.path.join(FILES_PATH, prefix_merge_dir, merge_file_name)
        ts_path = os.path.join(FILES_PATH, prefix_ts_dir)

        with open(merge_file, 'wb') as f_out:
            for ts_file_name in ts_file_name_list:
                ts_path_file_name = os.path.join(ts_path, ts_file_name)
                with open(ts_path_file_name, 'rb') as f_in:
                    f_out.write(f_in.read())

        # 删除ts目录下所有文件
        for ts_file_name in ts_file_name_list:
            os.remove(os.path.join(ts_path, ts_file_name))
    except Exception as ex:
        raise Exception('合并文件时，出现异常！')


def save_bytes(net_res, file_name, prefix_dir=None):
    try:
        _save_file = os.path.join(FILES_PATH, file_name)
        if prefix_dir is not None:
            _tmp_dir = os.path.join(FILES_PATH, prefix_dir)
            create_dir(_tmp_dir)
            _save_file = os.path.join(_tmp_dir, file_name)

        with open(_save_file, 'wb') as fs:
            fs.write(net_res.content)
        return True

    except Exception as ex:
        raise Exception('文件保存本地出现异常！')


def save_text(text, file_name, prefix_dir=None):
    try:
        _save_file = os.path.join(FILES_PATH, file_name)
        if prefix_dir is not None:
            _tmp_dir = os.path.join(FILES_PATH, prefix_dir)
            create_dir(_tmp_dir)
            _save_file = os.path.join(_tmp_dir, file_name)

        with open(_save_file, 'w') as fs:
            fs.write(text)
        return True
    except Exception as ex:
        return False


# 初始化存储目录
create_dir(FILES_PATH)
