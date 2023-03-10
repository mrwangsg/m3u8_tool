#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 22:15
# @Author  : sgwang
# @File    : setting.py
# @Software: PyCharm


# m3u8初始地址
m3u8_url_list = [

    # 'https://v11.tkzyapi.com/20211014/X8jAuzWN/index.m3u8',  # 第一集
    # 'https://v11.tkzyapi.com/20211014/0TTDJnzy/index.m3u8',  # 第二集
    # 'https://v11.tkzyapi.com/20211014/x519OC8D/index.m3u8',  # 第三集

]
init = {
    'thread_num': 6,  # 线程数
    'request_timeout': 15,  # 请求超时时长
    'delete_ts_dir': False,  # 请求结束后，是否删除ts文件夹
}
