#coding=utf-8

import urllib
import re
import sys
import os
import json
import requests

def getHtml(url):
    
    page = urllib.urlopen(url)
    html = page.read()
    return html


def getManyPages(keyword,pages):
    
    params=[]
    for i in range(30, 30 * pages + 30, 30):
        params.append({
                      'tn': 'resultjson_com',
                      'ipn': 'rj',
                      'ct': 201326592,
                      'is': '',
                      'fp': 'result',
                      'queryWord': keyword,
                      'cl': 2,
                      'lm': -1,
                      'ie': 'utf-8',
                      'oe': 'utf-8',
                      'adpicid': '',
                      'st': -1,
                      'z': '',
                      'ic': 0,
                      'word': keyword,
                      's': '',
                      'se': '',
                      'tab': '',
                      'width': '',
                      'height': '',
                      'face': 0,
                      'istype': 2,
                      'qc': '',
                      'nc': 1,
                      'fr': '',
                      'pn': i,
                      'rn': 30,
                      'gsm': '1e',
                      '1488942260214': ''
                  })
        
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        urls.append(requests.get(url, params=i).json().get('data'))
 
    return urls


def getImg(html, save_path, filename=""):
    
    if not os.path.exists(save_path):  # 新建文件夹
        os.mkdir(save_path)    
    
    reg =  r'"ObjURL":"(.*?.jpg)",'
    imgre = re.compile(reg, re.S)
    imglist = re.findall(imgre, html)
    
    print "image count %d"%(len(imglist))
    
    x = 0
    for imgurl in imglist:
        print imgurl
        new_file_path = os.path.join(save_path, '%s%d.jpg'%(filename, x))
        urllib.urlretrieve(imgurl, new_file_path)
        x += 1
        
    return imglist


def getImg2(dataList, localPath, filename=""):

    if not os.path.exists(localPath):  # 新建文件夹
        os.mkdir(localPath)

    x = 0
    for list in dataList:
        for i in list:

            if i.get('thumbURL') != None:
                print(u'正在下载：%s'%( i.get('thumbURL').encode('gbk')))
                ir = requests.get(i.get('thumbURL'))
                
                new_file_path = os.path.join(localPath, '%s%d.jpg'%(filename, x))
                with open(new_file_path, 'wb') as f:
                    f.write(ir.content)
                    
                x += 1
            else:
                print(u'图片链接不存在')


if __name__ == "__main__":
    
    dataList = getManyPages(u'头像', 30)  # 参数1:关键字，参数2:要下载的页数
    getImg2(dataList, "downloadimage", "image") # 参数2:指定保存的路径
        
    #url = r"http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1512801786479_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E5%A4%B4%E5%83%8F"
    #save_path = "downloadimage"
    #html = getHtml(url)
    #print html
    #getImg(html, save_path, 'head')