# coding=utf-8
"""
图片连接
"""

from common import *


class PicLink(UrlHandle):
    """
    获取具体的图片连接
    """
    def __init__(self, url):
        self.url = url

    def __get_html_text(self):
        """
        获取页面html文本
        :return: html文本
        """
        headers = {"User-Agent": "Mozilla/5.1 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
        request = self.get_request(self.url, headers)

        return urllib2.urlopen(request).read()

    def get_pic_link(self):
        """
        获取图片连接
        :return: 连接
        """
        html = etree.HTML(self.__get_html_text(), parser=etree.HTMLParser(encoding='gbk'))
        return html.xpath('//div[@class="pic"]/img/@src')[0]

    def xml(self):
        """
        组装成xml
        :return: XML字符串
        """
        link = self.get_pic_link()
        if link.startswith('http'):
            pass
        else:
            link = "http:" + link

        # 构建xml
        root = etree.Element("root")
        type = etree.SubElement(root, "type")
        type.set("msg", "1008")

        pic_elem = etree.SubElement(root, "pic")
        pic_elem.set("link", "data")
        pic_elem.text = link

        return etree.tostring(root, encoding='utf-8', pretty_print=True)

if __name__ == '__main__':
    p = PicLink("http://car.autohome.com.cn/photo/20191/3/2896325.html#pvareaid=2042264")
    print (p.xml())