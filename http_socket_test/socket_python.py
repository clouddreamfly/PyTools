#!/usr/bin/python
#coding:utf-8

import socket,sys
import time
import threading
import sitecustomize



def SocketConnect(addr = ('127.0.0.1', 8080),  write_content = False):
    
    try:
        sock = socket.socket()
        sock.connect(addr)

        if write_content == True : 
            sock.sendall('1234567890qwertyuiop[]asdfghjklzcxvbmnmfgfdffgdfadfs;') 
        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    except:
        print('error')
        #sock.shutdown(socket.SHUT_RDWR)
        sock.close()        
        return False
    
    return True

    
    
class SocketConnectThread(threading.Thread):
    
    def __init__(self, addr, write_content, thread_id, thread_name=u"socket connect test"):
        
        super(SocketConnectThread, self).__init__()
        
        self._addr = addr
        self._write_content = write_content
        self._thread_id = thread_id
        self._thread_name = thread_name
        self._connect_count = 0
        print thread_name
    
    def run(self):
        
        print u"线程ID:%d, 线程名称：%s, 已经启动！"%(self._thread_id, self._thread_name)   
        
        # 下载处理
        while True:
            self.ConnectThread()
            
        print u"线程ID:%d, 线程名称：%s, 即将结束！"%(self._thread_id, self._thread_name)   
    
    
    def ConnectThread(self):
    
        result = SocketConnect(self._addr, self._write_content)
        if result == True:
            self._connect_count += 1
            print u"链接成功, 线程ID:%d, 次数：%d"%(self._thread_id, self._connect_count)  
            time.sleep(0.05)
        else:
            print u"链接失败, 线程ID:%d"%(self._thread_id) 
            time.sleep(1)

        
        
    
if __name__ == "__main__":
    

    addr = raw_input(u"请输入addr：")
    port = raw_input(u"请输入port：")
    while True:
        if len(port) > 0 and port.isdigit():
            port = int(port)
            if port > 0:
                break
        else:
            port = raw_input(u"请重新输入port：")    
    
    write_content = raw_input(u"请输入是否发送内容(Y/N):")
    while True:
        if write_content in ('N', 'n'):
            write_content = False
            break
        elif write_content in ('Y', 'y'):
            write_content = True
            break
        else:
            write_content = raw_input(u"请输入是否发送内容(Y/N):")
            
    thread_count = 10
    thread_num = raw_input(u"请输入线程数(默认10)：")
    while True:
        if len(thread_num) == 0:
            break
        else:
            if thread_num.isdigit():
                thread_count = int(thread_num)
                if thread_count > 0:
                    break
            else:
                thread_num = raw_input(u"请重新输入线程数(默认10)：")
    
    # 线程处理
    connect_thread = []

    for i in range(thread_count):
        thread = SocketConnectThread((addr, port), write_content, i+1)
        connect_thread.append(thread)
        thread.start()
        
        
    for i in range(len(connect_thread)):
        connect_thread[i].join()
        
        
    print u"结束"
