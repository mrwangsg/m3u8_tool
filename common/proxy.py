#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/9 17:31
# @Author  : sgwang
# @File    : proxy.py
# @Software: PyCharm
import random

import requests


class proxy_pool:
    """
    IP代理池使用
    """
    __ip_http_proxy_pool = []
    __ip_https_proxy_pool = []

    def __init__(self):
        pass

    @classmethod
    def init_proxy_pool(cls):
        try:
            all_http_proxy = requests.get("http://127.0.0.1:5010/all/").json()
            for _ in all_http_proxy:
                proxy_ip = _.get("proxy")
                cls.__ip_http_proxy_pool.append({"http": "http://{}".format(proxy_ip)})

            all_https_proxy = requests.get("http://127.0.0.1:5010/all?type=https").json()
            for _ in all_https_proxy:
                proxy_ip = _.get("proxy")
                cls.__ip_https_proxy_pool.append({"https": "https://{}".format(proxy_ip)})

            print("...代理IP初始成功！...")
            print(cls.__ip_http_proxy_pool)
            print(cls.__ip_https_proxy_pool)
        except ConnectionError:
            print("...IP代理池服务，未启动。后续请求将不走代理IP...")
            return None
        except Exception:
            print("...代理IP获取失败！...")
            return None

    @classmethod
    def http_proxy_ip(cls):
        """
        随机获取代理IP
        :return:
        """
        if len(cls.__ip_http_proxy_pool) == 0:
            return None
        return cls.__ip_http_proxy_pool[random.randint(0, len(cls.__ip_http_proxy_pool) - 1)]

    @classmethod
    def https_proxy_ip(cls):
        """
        随机获取代理IP
        :return:
        """
        if len(cls.__ip_https_proxy_pool) == 0:
            return None
        return cls.__ip_https_proxy_pool[random.randint(0, len(cls.__ip_https_proxy_pool) - 1)]


proxy_pool.init_proxy_pool()

if __name__ == "__main__":
    print(proxy_pool.http_proxy_ip())
    print(proxy_pool.https_proxy_ip())
