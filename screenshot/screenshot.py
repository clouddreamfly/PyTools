#!/usr/bin/python3
#-*- coding:utf-8 -*-


from PIL import ImageGrab
import datetime #导入datetime库用于生成带时间的图片名

x1 = 0
y1 = 0
x2 = 800
y2 = 600
box = (x1, y1, x2, y2)
# x1: 开始截图的x坐标;x2:开始截图的y坐标;x3:结束截图的x坐标;x4:结束截图的y坐标

#获取当前时间,转化成字符串
timenow = datetime.datetime.now()
timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")

imgname = "screenshot_" + timestr + ".png"
img = ImageGrab.grab(box)
img.save(imgname) #保存截图文件的路径
