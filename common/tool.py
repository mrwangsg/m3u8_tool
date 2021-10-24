#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/10/20 22:11
# @Author  : sgwang
# @File    : tool.py
# @Software: PyCharm
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import m3u8
import requests
from requests.adapters import HTTPAdapter

from common import file_util
from common.proxy import proxy_pool


def get_headers():
    """
    返回请求头
    :return:
    """
    return {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 7 Build/MOB30X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
    }


def download_file_ts(req_session, uri, file_name, prefix_dir=None):
    try:
        headers = get_headers()
        proxies = proxy_pool.http_proxy_ip()
        res = req_session.get(uri, timeout=30, headers=headers, proxies=proxies, verify=True)

        if res.status_code == 200:
            return file_util.save_bytes(res, file_name, prefix_dir)

        raise Exception('响应码不是200，无法解析内容！')
    except Exception as ex:
        raise ex


def use_thread_pool(pool, retry, req_session, tasks, ts_files_local_dir):
    print("=" * 20, retry, "=" * 20)
    results, tmp_tasks = [], tasks

    # 创建任务
    for _01 in tmp_tasks:
        ts_uri, ts_file_name = _01.get('ts_uri'), _01.get('ts_file_name')
        # 将ts文件下载到本地
        result = pool.submit(download_file_ts, req_session, ts_uri, ts_file_name, ts_files_local_dir)
        results.append({
            'ts_uri': ts_uri,
            'ts_file_name': ts_file_name,
            'result': result,
        })

    # 清空循环任务表
    tmp_tasks = []

    # 检查任务结果
    for index, _02 in enumerate(results):
        ts_uri, ts_file_name = _02.get('ts_uri'), _02.get('ts_file_name')
        if _02.get('result').exception():
            print("异常抛出：", _02.get('result').exception(), str(ts_uri))
            tmp_tasks.append({
                'ts_uri': ts_uri,
                'ts_file_name': ts_file_name,
            })
        print('\r当前结果下标{}，进度{}%'.format(index, (index * 100 // len(results))), end="")

    print("=" * 20, retry, "=" * 20)
    return tmp_tasks


class RequestsClient:
    def download(self, uri, timeout=None, headers=dict, verify_ssl=True):
        headers = get_headers()
        proxies = proxy_pool.http_proxy_ip()
        # print('proxies:', proxies)

        res = requests.get(uri, timeout=timeout, headers=headers, proxies=proxies, verify=True)
        return res.text, res.url


def filter_has_req_tasks(tasks, ts_files_local_dir):
    ret_tasks = []
    ts_files = file_util.list_dir_file(ts_files_local_dir)

    for _ in tasks:
        if _.get('ts_file_name') not in ts_files:
            ret_tasks.append(_)

    return ret_tasks


def merge_flag(task, ts_files_local_dir):
    ts_files = file_util.list_dir_file(ts_files_local_dir)

    if len(ts_files) == len(task):
        return True
    return False


def parsed_m3u8_uri(uri: str):
    """

    :param uri:
    :return: 主机地址，资源全路径，资源文件名，资源路径(不包含文件名)
    """
    base_uri = str(uri)
    parsed_uri = urlparse(base_uri[:-1]) if base_uri.endswith('/') else urlparse(base_uri)

    # 主机地址，资源全路径，资源文件名，资源路径(不包含文件名)
    base_host_name = str(f'{parsed_uri.scheme}://{parsed_uri.netloc}')
    base_path_file_name = str(f'{parsed_uri.path}')
    base_file_name = re.search(r'[^/\\w]*.m3u8', base_path_file_name).group()
    base_path_name = base_path_file_name.replace(base_file_name, '')

    return base_host_name, base_path_file_name, base_file_name, base_path_name


def just_req_ts_file(req_session, thread_num, hls_files_ts, is_variant=False):
    base_host_name, base_path_file_name, base_file_name, base_path_name = parsed_m3u8_uri(str(hls_files_ts.base_uri))

    # hls文件，本地存储路径
    hls_local_dir = base_path_name.replace('/', '_')
    file_util.save_text(hls_files_ts.dumps(), base_file_name, hls_local_dir)

    # ts文件，本地存储路径
    ts_files_local_dir = hls_local_dir + os.sep + "ts"

    # 整理好任务
    tasks = []
    for _ts in hls_files_ts.files:
        ts_uri = base_host_name + base_path_name + str(_ts)
        if is_variant:
            ts_uri = base_host_name + base_path_name + str(_ts).split('/')[-1]
        tasks.append({
            'ts_uri': ts_uri,
            'ts_file_name': str(_ts).split('/')[-1],
        })
    filter_tasks = filter_has_req_tasks(tasks, ts_files_local_dir)

    # 使用线程池
    with ThreadPoolExecutor(max_workers=thread_num) as pool:
        tmp_tasks = filter_tasks
        for retry in range(3):
            if len(tmp_tasks) == 0:
                break
            tmp_tasks = use_thread_pool(pool, retry, req_session, tmp_tasks, ts_files_local_dir)

    # 将所有ts文件，合并到一个文件中
    if merge_flag(tasks, ts_files_local_dir):
        ts_file_name_list, merge_files_ts = [], base_file_name + "_.ts"
        for _ in tasks:
            ts_file_name_list.append(_.get('ts_file_name'))
        file_util.merge_all_ts(merge_files_ts, hls_local_dir, ts_files_local_dir, ts_file_name_list)
        print("合并ts文件结束！")
    else:
        print('ts文件不足，无法合并！！！')


def main_seed_url(url: str, thread_num: int = 2):
    # http https 分别对应各自类型，只是需要分别设置连接数
    req_session = requests.Session()
    conn_num = thread_num * 2
    req_session.mount('https://', HTTPAdapter(pool_connections=conn_num, pool_maxsize=conn_num))
    req_session.mount('http://', HTTPAdapter(pool_connections=conn_num, pool_maxsize=conn_num))

    basic_video = m3u8.load(url, http_client=RequestsClient())
    print('base_uri:', basic_video.base_uri)

    # 媒体播放列表
    if basic_video.is_variant:
        for hls_playlist in basic_video.playlists:
            # 主机地址，资源全路径，资源文件名，资源路径(不包含文件名)
            base_host_name, base_path_file_name, base_file_name, base_path_name = parsed_m3u8_uri(
                str(basic_video.base_uri))

            # hls文件，全路径地址
            hls_playlist_uri = base_host_name + hls_playlist.uri
            print('hls_playlist_uri:', hls_playlist_uri)

            # 请求获取hls，获取ts文件信息列表
            hls_files_ts = m3u8.load(hls_playlist_uri, http_client=RequestsClient())
            just_req_ts_file(req_session, thread_num, hls_files_ts, is_variant=True)
    else:
        just_req_ts_file(req_session, thread_num, basic_video)
