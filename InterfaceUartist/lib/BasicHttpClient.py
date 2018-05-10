#-*- coding:utf-8 -*-
import http.client
import logging
from InterfaceUartist.common.Logging import Logging

class BasicHttpClient:
    """
    http.client 封装
    http管理类
    """
    def __init__(self, protocol, host, port=80,
                 key_file=None, cert_file=None,
                 timeout=30, log_level=logging.INFO):
        '''
        :param protocol: 协议http或https 
        :param host: 地址
        :param port: 端口，默认80
        :param key_file: 密钥 SSL
        :param cert_file: 证书 SSL
        :param timeout: 超时时间
        :param log_level: 日志级别
        '''
        self.log_level = log_level
        self.log = Logging(level=log_level)
        self.log.output("初始化http连接到：%s:%d" % (host,port))

        self.host = host
        self.port = port
        self.timeout = timeout
        self.key_file = key_file
        self.cert_file = cert_file

        self.response = None
        self.data = None
        self.status =None
        self.reason = None
        self.headers = None
        self.http = None

        if protocol == "http":
            self.http = http.client.HTTPConnection(
                host=self.host, port=self.port, timeout=self.timeout
            )
        elif protocol == "https":
            self.http = http.client.HTTPSConnection(
                host=self.host, port=self.port,
                key_file=self.key_file, cert_file=self.cert_file,
                timeout=self.timeout
            )
        else:
            print("不支持的协议类型：", protocol)
            exit()

    def request(self, method, url, body=None, headers={}):
        '''
        返回response响应对象
        :param method: 请求方法
        :param url: 请求url
        :param body: 请求数据
        :param headers: 请求头
        :return: response
        '''
        self.http.request(
            method=method, url=url, body=body, headers=headers
        )
        self.response = self.http.getresponse()

        self.data = self.response.read()
        self.status = self.response.status
        self.reason = self.response.reason
        self.headers = self.response.getheaders()

        self.log.output("------"*10, self.log_level)
        self.log.output("\nrequest")
        self.log.output("\nurl: %s \nmethod: %s \nheaders: %s ""\ndata: %s" %  (url, method, headers, body), self.log_level)
        self.log.output("\nresponse")
        self.log.output("\nstatus: %s \nreason: %s \nheaders: %s ""\ndata: %s" %  (self.status, self.reason, self.headers, self.data), self.log_level)

        return self.response

    def close(self):
        '''
        关闭连接
        :return: 
        '''
        if self.http:
            self.http.close()

    def get_data(self):
        '''
        返回响应内容
        :return: self.data
        '''
        return self.data

    def get_header(self, name):
        '''
        返回指定响应头
        :param name: 响应头参数名称
        :return: 
        '''
        for header in self.headers:
            if header[0] == name:
                return header[1]
        return None

    def get_headers(self):
        '''
        返回完整响应头列表
        :return: self.headers
        '''
        return self.headers

    def get_status_reason(self):
        '''
        返回状态码和说明文本
        :return: self.status  self.reason
        '''
        return (self.status, self.reason)