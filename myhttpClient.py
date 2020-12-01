# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     httpClient
   Description :
   Author :       seven
   date：          2020/11/27
-------------------------------------------------
   Change Activity:
                   2020/11/27:
-------------------------------------------------
"""
__author__ = 'seven'

# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'seven'

import urllib.request
import http.cookiejar
import urllib.parse
import time
import socket
socket.setdefaulttimeout(20)
class MyHttp(object):
    '''配置要测试请求服务器的ip、端口、域名等信息，封装http请求方法，http头设置'''

    def __init__(self,timeout,header={}):
        # 从配置文件中读取接口服务器IP、域名，端口

        self.headers = header  # http 头
        self.timeout=timeout

        # install cookie #自动管理cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPHandler,urllib.request.HTTPSHandler,urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

    # 设置http头
    def set_header(self, headers):
        self.headers = headers

    # 封装HTTP GET请求方法
    def get(self, url, params=''):
        i=0
        while i<=2:
        #url = self.protocol + '://' + self.host + ':' + str(self.port) + url + params

            print('发起的请求为：%s' % url)
            request = urllib.request.Request(url, headers=self.headers)
            try:
                response = urllib.request.urlopen(request)
                return response
            except Exception as e:
                print('发送请求失败，原因：%s, 开始重连' % e)
                time.sleep(2)
                i=i+1
        return None

    # 封装HTTP POST请求方法
    def post(self, url, data):

        i=0
        while i<=2:
        #url = self.protocol + '://' + self.host + ':' + str(self.port) + url
            print('发起的请求为：%s' % url)
            request = urllib.request.Request(url, headers=self.headers)
            try:
                response = urllib.request.urlopen(request, data.encode())
                return response
            except Exception as e:
                print('发送请求失败，原因：%s, 开始重连' % e)
                time.sleep(2)
                i=i+1
        return None