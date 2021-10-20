#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 15:23
# @Author  : sgwang
# @File    : main.py
# @Software: PyCharm
import sys
import time
import traceback

import setting
from common import tool


def main():
    m3u8_url_list = setting.m3u8_url_list
    thread_num = setting.thread_num

    for url in m3u8_url_list:
        tool.main_seed_url(url, thread_num)
        print("=" * 40)
        print()
        print()
    print('程序运行结束...')


if __name__ == "__main__":
    print('hello, m3u8!')

    start_time = time.time()
    try:
        main()

    except Exception as ex:
        print(traceback.format_exc())
    finally:
        print(f'the program running time is: {int(time.time() - start_time)}s')
        sys.exit(0)
