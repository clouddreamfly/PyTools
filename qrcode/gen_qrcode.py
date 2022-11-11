#!/usr/bin/python3
#-*- coding:utf-8 -*-

import qrcode   #导入qrcode库, 用于生成二维码
import datetime #导入datetime库用于生成带时间的图片名
import os

#输入待转换的字符串
qrstr = input("Enter the string to be converted:")
print("Input :" + qrstr)

#采用默认方式生成二维码
qr = qrcode.QRCode()
qr.add_data(qrstr)
qrimg = qr.make_image(back_color='TransParent')

#获取当前时间,转化成字符串
timenow = datetime.datetime.now()
timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")

#保存二维码图片
qrname = "qrcode" + timestr + '.png'
qrimg.save(qrname)
print("Success!")