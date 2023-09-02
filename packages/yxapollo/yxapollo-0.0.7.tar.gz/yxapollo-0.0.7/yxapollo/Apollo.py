#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
from .ApolloClient import ApolloClient


class Apollo:
    def __init__(self, appid, config_server_url, cluster='default'):
        self.appid = appid
        self.config_url = config_server_url
        self.apollo = ApolloClient(app_id=self.appid, config_server_url=self.config_url, cluster=cluster)
        self.apollo.start()

    def get_value(self, key, namespace="application", default_val=None):
        """
        获取指定appid下指定namespace下的指定key的值
        :param key: 参数
        :param namespace: 参数集合
        :param default_val: 默认值
        :return: value
        """
        try:
            return self.apollo.get_value(key=key, namespace=namespace, default_val=default_val)
        except Exception as e:
            return None

    def get_all_values_no_cache(self, appid, namespace="application"):
        """
        通过不带缓存的Http接口从Apollo读取配置
        :return: 指定namespace下的全部数据 dict
        """
        url = '{}/configs/{}/{}/{}?ip={}'.format(self.config_url, appid, "default", namespace, "0.0.0.0")
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()['configurations']
        else:
            return {}
