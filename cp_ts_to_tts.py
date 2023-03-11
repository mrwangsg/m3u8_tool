#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/3/10 21:10
# @Author  : sgwang
# @File    : cp_ts_to_tts.py
# @Software: PyCharm

import os
import shutil

from common import file_util

# 目的是将目录files下，所有合成的ts文件，提取出来。暂存到tss目录下的子目录，该子目录由创建时间戳来命名
if __name__ == "__main__":
    print('hello, m3u8!')

    # 先创建tss保存目录
    ts_save_dir, task_ts_path_list, copy_ts_path_list = str(file_util.FILES_PATH + os.sep + "tss"), [], []
    shutil.rmtree(ts_save_dir)
    file_util.create_dir(ts_save_dir)

    # 准备要打开的保存有ts文件的目录
    for dir_file in os.listdir(file_util.FILES_PATH):
        dir_file_path = file_util.FILES_PATH + os.sep + dir_file

        # 排除自建的tss目录
        if os.path.isdir(dir_file_path) and dir_file != 'tss':
            # print('dir:', dir_file)
            task_ts_path_list.append(dir_file_path)

    # 遍历任务，准备复制文件
    for _task_ts_path in task_ts_path_list:
        _inner_dir_file_list = os.listdir(_task_ts_path)
        for _inner_dir_file in _inner_dir_file_list:
            _inner_dir_file_path = _task_ts_path + os.sep + _inner_dir_file

            # 如果是ts文件，进行复制操作
            if os.path.isfile(_inner_dir_file_path) and str(_inner_dir_file_path).endswith('.ts'):
                # print(_inner_dir_file_path)
                copy_ts_path_list.append({"file": _inner_dir_file, "path": _inner_dir_file_path})

    # 操作复制任务
    for _index, _copy_ts in enumerate(copy_ts_path_list):
        source_path = _copy_ts.get('path')
        dest_path = ts_save_dir + os.sep + str(_index + 1) + "_" + _copy_ts.get('file')
        print("source_path: ", source_path, "dest_path: ", dest_path)
        shutil.copy(source_path, dest_path)

    pass
