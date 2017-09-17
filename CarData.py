# coding=utf-8
"""
获取车辆模块
"""
from common import *


class CarData(UrlHandle):
    """
    车辆数据类,针对车辆具体数据的处理
    """

    def __init__(self, id):
        self.html = None
        self.id = id
        self.onSale_list = []
        self.offSale_list = []
        self.htmlText = self.__get_html_text()

    def __get_html_text(self, url=None):
        """
        获取html文本
        :return: html页面文本
        """
        if url is None:
            url = "http://www.autohome.com.cn/" + self.id + "/"
        headers = {"User-Agent": "Mozilla/5.1 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}
        request = self.get_request(url, headers)

        return urllib2.urlopen(request).read()

    def on_sale(self):
        """
        获取在售车辆数据,包括车辆具体年款,配置及对应ID
        :return: [("2017款 1.5T 自动舒适版", 2231),("2017款 1.5T 自动舒适版", 2231)]
        """
        if self.html is None:
            self.html = etree.HTML(self.htmlText, parser=etree.HTMLParser(encoding='gbk'))

        # 获取在售车辆名
        name_list = self.html.xpath('//p[@data-gcjid]/a/text()')

        # 获取在售车辆id
        id_list = self.html.xpath('//p[@data-gcjid]/@data-gcjid')

        self.onSale_list = zip(id_list, name_list)

    def off_sale(self):
        """
        获取停售款所有数据
        :return: [("2017款 1.5T 自动舒适版", 2231),("2017款 1.5T 自动舒适版", 2231)]
        """
        if self.html is None:
            self.html = etree.HTML(self.htmlText, parser=etree.HTMLParser(encoding='gbk'))

        # 停售所有年款名
        year_list = self.html.xpath('//a[@pageflag="False"]/text()')

        # 对应的年款data
        data_list = self.html.xpath('//a[@pageflag="False"]/@data')

        # 年款要与年款数据长度一致
        if len(year_list) != len(data_list):
            print ("停售数据有异常")
            return

        for data in data_list:
            url = 'http://www.autohome.com.cn/ashx/series_allspec.ashx?s=' + self.id + '&y=' + data
            json_text = self.__get_html_text(url=url)

            # 将json转换为python字典
            data_dict = (json.loads(json_text.decode('gbk').encode('utf-8')))

            # 获取字典中车辆信息,Spec是个列表数据,每个元素是列表
            car_list = data_dict['Spec']

            # car_list是列表,但里面的每个元素是字典,最终把数据加入到成员变量中
            for spec_car in car_list:
                self.offSale_list.append((str(spec_car['Id']), spec_car['Name']))

    def xml(self):
        """
        将在售车辆与停售车辆组装成xml字符串
        :return: xml字符串
        """
        if (self.onSale_list is None) and (self.offSale_list is None):
            print ("在售车辆与停售车辆数据异常")
            return

        root = etree.Element("root")
        type = etree.SubElement(root, "type")
        type.set("msg", "1004")

        # 组装在售数据
        on_sale = etree.SubElement(root, "OnSale")
        for car in self.onSale_list:
            elem = etree.SubElement(on_sale, "Car")
            elem.set("id", car[0])
            elem.text = car[1]

        # 组装停售数据
        off_sale = etree.SubElement(root, "offSale")
        for car in self.offSale_list:
            elem = etree.SubElement(off_sale, "Car")
            elem.set("id", car[0])
            elem.text = car[1]

        return etree.tostring(root, encoding='utf-8', pretty_print=True)


if __name__ == '__main__':
    c = CarData('2945')
    c.off_sale()
    c.on_sale()

    print c.xml()

