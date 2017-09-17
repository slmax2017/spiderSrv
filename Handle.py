# coding=utf-8
"""
具体业务处理模块,通过网络模块传入数据
"""
from brands import *
from CarData import *
from spiderPic import *
from picLink import *


def brands_handle(conn, root):
    """
    车辆品牌,车系数据获取,并发送
    :param conn: 客户socket
    :param root: xml根节点
    :return: None
    """

    # 获取品牌拼音首字母
    brand = root.find('brand')
    x = brand.text

    # 构建品牌模块对象.获取xml数据
    b = Brands(x)
    data = b.xml()
    length = len(data) + 100000

    # 发送数据至QT
    conn.send(str(length))
    conn.send(data)


def car_data_handle(conn, root):
    """
    获取车辆名,对应ID
    :param conn: 客户socket
    :param root: xml根节点
    :return:None
    """

    # 获取车系编号
    id = root.find("CarID")
    car = id.text

    # 构建车系对象,获取在售停售所有数据
    c = CarData(car)
    c.on_sale();
    c.off_sale()
    data = c.xml()
    length = len(data) + 100000

    print (data)
    # 发回数据致QT
    conn.send(str(length))
    conn.send(data)


def pic_handle(conn, root):
    """
    图片获取
    :param conn: 客户socket
    :param root: xml根节点
    :return: Node
    """

    # 获取车辆编号
    id1 = root.find("CarID")
    spec_car = id1.text

    # 获取图片连接
    s = SpiderPic(spec_car)
    s.get_main_link()
    s.get_type_link()
    data = s.xml()
    length = len(data) + 100000

    print (data)
    # 发回给QT
    conn.send(str(length))
    conn.send(data)


def extract_link(conn, root):
    """
    提取图片连接,发回给QT
    :param conn: 客户socket
    :param root: xml根节点
    :return:
    """
    url = root.find('pic')

    # 创建对象
    p = PicLink(url.text)
    data = p.xml()
    length = len(data) + 100000

    print (length)
    print (data)

    # 发回给QT
    conn.send(str(length))
    conn.send(data)


def handle(conn, xml):
    """
    业务处理分发器
    :param conn: 客户socket
    :param xml:  xml字符串
    :return: None
    """
    root = ET.fromstring(xml)
    type = root.find('type')
    opt = type.attrib['msg']

    if opt == "1001":
        brands_handle(conn, root)
    elif opt == "1003":
        car_data_handle(conn, root)
    elif opt == "1005":
        pic_handle(conn, root)
    elif opt == "1007":
        extract_link(conn, root)



if __name__ == '__main__':
    xml = '<root data="汽车数据"><type msg="1">aaa</type></root>'
    handle(None, xml)


