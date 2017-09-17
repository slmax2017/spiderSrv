# coding=utf-8
"""
爬取图片模块
"""
from common import *


class SpiderPic(UrlHandle):
    """
    图片爬取类
    """
    def __init__(self, id):
        self.html = None
        self.id = id
        self.pic_link = None
        self.pic_type = []

    def __get_html_text(self, url=None):
        """
        获取页面html文本
        :return: html文本
        """
        if url is None:
            url = 'http://www.autohome.com.cn/spec/' + self.id + '/'
        headers = {"User-Agent": "Mozilla/5.1 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
        request = self.get_request(url, headers)

        return urllib2.urlopen(request).read()

    def get_main_link(self):
        """
        获取图片主页连接
        :return:link
        """
        self.html = etree.HTML(self.__get_html_text(), parser=etree.HTMLParser(encoding='gbk'))

        # 获取图片主页连接
        self.pic_link = self.html.xpath('//div[@class="subnav"]/div/ul/li[3]/a/@href')

        # 组装连接
        self.pic_link[0] = "http:" + self.pic_link[0]

        return self.pic_link

    def get_type_link(self):
        """
        获取图片分类连接
        :return: [(link, name),(link, name)]
        """
        if self.pic_link is None:
            print ("图片主页数据为空")
            return

        html = etree.HTML(self.__get_html_text(url=self.pic_link[0]), parser=etree.HTMLParser(encoding='gbk'))

        # 获取图片分类连接
        link_list = html.xpath('//div[@class="search-pic"]/div/ul[@class="search-pic-sortul"]/li/a/@href')

        # 图片分类名称
        name_list = html.xpath('//div[@class="search-pic"]/div/ul[@class="search-pic-sortul"]/li/a/text()')

        # 组装图片分类连接
        for i in range(0, len(link_list)):
            link_list[i] = "http://car.autohome.com.cn" + link_list[i]

        self.pic_type = zip(name_list, link_list)
        return self.pic_type

    def get_links(self, pic_url):
        """
        根据分类连接获取所有图片连接
        :param pic_url: 分类连接url
        :return: 连接列表[(name,pic_link)]
        """
        html = etree.HTML(self.__get_html_text(url=pic_url), parser=etree.HTMLParser(encoding='gbk'))
        return html.xpath('//div[@class="row"]//ul/li/a[@title]/@href')

    def xml(self):
        """
        将图片连接组装为xml
        :return: xml
        """

        # 构建xml
        root = etree.Element("root")
        type = etree.SubElement(root, "type")
        type.set("msg", "1006")

        for item in self.pic_type:
            links = self.get_links(item[1])
            name = etree.SubElement(root, 'name')
            name.set('kind', item[0])
            for link in links:
                url = "http://car.autohome.com.cn" + link
                href = etree.SubElement(name, "href")
                href.set("link", u'汽车链接')
                href.text = url

        return etree.tostring(root, encoding='utf-8', pretty_print=True)

if __name__ == '__main__':
    s = SpiderPic('20191')
    s.get_main_link()
    s.get_type_link()
    print s.xml()