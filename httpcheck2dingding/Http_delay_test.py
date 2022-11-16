# -*- coding: utf-8 -*-

import requests
import json
import time
from urllib.parse import urlparse

url = "https://api.test.com/api/info/activity?channelCode=21010810001"
domain = "{uri.netloc}".format(uri=urlparse(url))
dingding_url= "https://oapi.dingtalk.com/robot/send?access_token=f9656scfbe5bbdb7f10e88be253b4b03be03e624269689cde9b"

def dingding_sender(logstr):
    headers = {"Content-Type": "application/json"}
    api_url = dingding_url
    data = {
     "msgtype": "text",
        "text": {
            "content": logstr
        },
    }
    requests.post(url=api_url, headers=headers,data=json.dumps(data))



def handleRequestTime(url):
    
    try:
        begin_time = time.time()
        response  = requests.get(url)
        end_time = time.time()
        response_time1 = response.elapsed.total_seconds()
        response_time2 = end_time - begin_time
        
        print(domain, "Conection OK.")
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logstr = "{0} {1} 响应时间为 {2:.6f}:{3:.6f} 秒。\n日期时间：{4}".format(domain, response.status_code, response_time1, response_time2, datetime)
        print(logstr)
        
        if response_time1 > 2 and response_time2 > 2:
            dingding_sender(logstr)
            
    except requests.exceptions.Timeout:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logstr = "{0} 连接超时.\n日期时间：{1}".format(domain, datetime)
        print(logstr)
        dingding_sender(logstr)
    except requests.exceptions.TooManyRedirects:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logstr = "{0} 出现重定向过多.\n日期时间：{1}".format(domain, datetime)
        print(logstr)
        dingding_sender(logstr)
    except requests.exceptions.RequestException as e:
        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logstr = "{0} 其他错误，访问出错.\n日期时间：{1}".format(domain, datetime)
        print(e)    


if __name__ == "__main__":

	while 1:
		
		handleRequestTime(url)
		time.sleep(30)

