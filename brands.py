# coding=utf-8
"""
分类品牌模块
"""
from common import *


class Brands(UrlHandle):
    """
    该类主要用于获取车辆品牌,
    车系名称及ID,
    并利用相关方法组装成XML的功能
    """

    def __init__(self, first_x):
        self.html = None
        self.firstChar = first_x
        self.brands_data = {} # 品牌数据
        self.car_data = []    # 车系数据

    def __get_html_text(self):
        """
        获取html文本
        :return: html页面文本
        """
        if len(self.firstChar) != 1:
            """
            品牌字母检查
            """
            print ("传入的品牌字母不正确")
            return None

        url = "http://www.autohome.com.cn/grade/carhtml/" + self.firstChar + ".html"
        headers = {"User-Agent": "Mozilla/5.1 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}

        request = self.get_request(url, headers)

        return urllib2.urlopen(request).read()

    def get_brands(self):
        """
        根据传入的汽车品牌首字母爬取该品牌汽车及以下车系所有车
        :return: ({品牌1:ID1},{品牌2:ID2}, html)
        """

        # 获取html文本
        data = self.__get_html_text()

        self.html = etree.HTML(data, parser=etree.HTMLParser(encoding='gbk'))
        brands_list = self.html.xpath("//dl/dt/div/a/text()")
        brands_node_list = self.html.xpath("//dl")

        for i in range(0, len(brands_list)):
            self.brands_data[brands_list[i]] = brands_node_list[i]

        return self.brands_data

    def get_car(self, brands_node):
        """
        根据品牌ID获取旗下的车系数据
        :param brands_node: 品牌元素
        :return: [("C4L",1), ("C5",2)]
        """
        # 汽车名列表
        lst_car_name = brands_node.xpath('.//h4/a/text()')

        # 汽车ID列表
        lst_car_id = brands_node.xpath('.//li/@id')

        # 清理ID号前面的s
        for i in range(0, len(lst_car_id)):
            lst_car_id[i] = lst_car_id[i][1:]

        # 两列表合并为,元组列表
        self.car_data = zip(lst_car_id, lst_car_name)
        return self.car_data

    def xml(self):
        """
        将品牌及车系数据打包成xml,便于发送
        :return: xml字符串
        """
        data = self.get_brands()
        if data is None:
            return

        root = etree.Element('root')
        root.set("data", u'汽车数据')
        type = etree.SubElement(root, "optType")
        type.set("msg", "1002")

        for item in data.items():
            brands_node = item[1]
            self.car_data = self.get_car(brands_node)
            brands = etree.SubElement(root, "brands")
            brands.set("name", item[0])

            for car_item in self.car_data:
                car = etree.SubElement(brands, "car")
                car.set("id", car_item[0])
                car.text = car_item[1]

        return etree.tostring(root, pretty_print=True, encoding='utf-8')

    def print_data(self):
        """
        打印汽车数据, 调试使用
        :return: NONE
        """
        data = self.get_brands()

        for item in data.items():
            id = item[1]
            car_data = self.get_car(id)
            print (u'品牌:' + item[0] + "     id:" + item[1])
            for car_item in car_data:
                print ("      " + car_item[1] + "       id:" + car_item[0])


if __name__ == '__main__':
    b = Brands('a')
    print b.xml()






