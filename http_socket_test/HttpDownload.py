# -*- coding: utf-8 -*-


import urllib2
import urllib
import time
import threading
import sitecustomize



def HttpDownload(url, read_content = False):
    
    try:
        response = urllib2.urlopen(url)
        if read_content: response.read()
    except:
        return False
    
    return True

    
    
class HttpDownloadThread(threading.Thread):
    
    def __init__(self, url, read_content, thread_id, thread_name=u"http download"):
        
        super(HttpDownloadThread, self).__init__()
        
        self._url = url
        self._read_content = read_content
        self._thread_id = thread_id
        self._thread_name = thread_name
        self._download_count = 0
        print thread_name
    
    def run(self):
        
        print u"线程ID:%d, 线程名称：%s, 已经启动！"%(self._thread_id, self._thread_name)   
        
        # 下载处理
        while True:
            self.DownloadThread()
            
        print u"线程ID:%d, 线程名称：%s, 即将结束！"%(self._thread_id, self._thread_name)   
    
    
    def DownloadThread(self):
    
        result = HttpDownload(self._url, self._read_content)
        if result == True:
            self._download_count += 1
            print u"下载成功, 线程ID:%d, 次数：%d"%(self._thread_id, self._download_count)    
        else:
            print u"下载失败, 线程ID:%d"%(self._thread_id) 
            time.sleep(1)

        
        
    
if __name__ == "__main__":
    

    url = raw_input(u"请输入URL：")
    read_content = raw_input(u"请输入是否读取内容(Y/N):")
    while True:
        if read_content in ('N', 'n'):
            read_content = False
            break
        elif read_content in ('Y', 'y'):
            read_content = True
            break
        else:
            read_content = raw_input(u"请输入是否读取内容(Y/N):")
            
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
    download_thread = []

    for i in range(thread_count):
        thread = HttpDownloadThread(url, read_content, i+1)
        download_thread.append(thread)
        thread.start()
        
        
    for i in range(len(download_thread)):
        download_thread[i].join()
        
        
    print u"结束"