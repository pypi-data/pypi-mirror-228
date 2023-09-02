#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import requests
from .ApolloClient import ApolloClient


class Apollo:
    def __init__(self, appid, config_server_url):
        self.appid = appid
        self.config_url = config_server_url
        self.apollo = ApolloClient(app_id=self.appid, config_server_url=self.config_url)
        self.apollo.start()

    def get_value(self, key, namespace="application"):
        """
        获取指定appid下指定namespace下的指定key的值
        :param appid: apollo appid
        :param key:
        :param namespace:
        :return: value
        """
        try:
            return self.apollo.get_value(key=key, namespace=namespace)
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
