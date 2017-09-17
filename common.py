# coding=utf-8

import urllib2
from lxml import etree
import xml.etree.ElementTree as ET
import json


class UrlHandle(object):
    """
    urllib2基类,
    """
    @staticmethod
    def get_request(url, headers):
        """
        获取request
        :param url: url
        :param headers: headers
        :return:
        """
        proxy_handler = urllib2.ProxyHandler({"http": "192.168.1.154:808"})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)

        return urllib2.Request(url, headers=headers)