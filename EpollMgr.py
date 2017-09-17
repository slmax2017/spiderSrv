# coding=utf-8
"""
网络主模块,用于接受信息,发送信息,程序主入口
"""

import select
import socket
from Handle import *


listen_socket = socket.socket()
listen_socket.bind(('', 9999))
listen_socket.listen(2)

sock_list = [listen_socket]

while True:
    readble, writeble, expble = select.select(sock_list, [], [])

    for conn in readble:
        # 有新客户加入
        if conn == listen_socket:
            cli, addr = listen_socket.accept()
            sock_list.append(cli)
        else:
            try:
                data = conn.recv(1024)
                print (data)

                # 业务处理
                handle(conn, data)
            except Exception as e:
                print (e)
                conn.close()
                sock_list.remove(conn)




