#!/usr/bin/python3
#-*- coding:utf-8 -*-

import qrcode   #导入qrcode库, 用于生成二维码
import datetime #导入datetime库用于生成带时间的图片名
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import ImageQt



def gen_qrcode(qrstr):
    
    #采用默认方式生成二维码
    qr = qrcode.QRCode()
    qr.add_data(qrstr)
    qrimg = qr.make_image(back_color = 'TransParent')
    
    return qrimg




class GenQrcodeFrame(QWidget):
    """"""

    def __init__(self):
        """Constructor"""
        
        super().__init__()
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle("二维码生成器")
        self.resize(580, 420)

        self.label1 = QLabel("输入生成信息：", self)
        self.txt_edit1 = QLineEdit("https://qr.test.com", self)
        
        self.group2 = QGroupBox("显示二维码图如下：", self)
        self.image2 = QLabel(",sdfs", self.group2)
        
        self.genQrcode()
        
        glayout = QVBoxLayout()
        glayout.addWidget(self.image2, 0, Qt.AlignCenter)
        self.group2.setLayout(glayout)
        
        self.btn_gen3 = QPushButton("生成", self)
        self.btn_save3 = QPushButton("保存", self)
        self.btn_gen3.setFixedSize(80, 36)
        self.btn_save3.setFixedSize(80, 36)
        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        
        layout1.addWidget(self.label1)
        layout1.addWidget(self.txt_edit1)
        
        layout2.addWidget(self.group2)
        
        layout3.addWidget(self.btn_gen3)
        layout3.addWidget(self.btn_save3)
        
        layout.addLayout(layout1)
        layout.addSpacing(10)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        
        self.setLayout(layout)
        
        self.btn_gen3.clicked.connect(self.onClickedGen)
        self.btn_save3.clicked.connect(self.onClickedSave)
        
        
    def genQrcode(self, qrstr = "https://qr.test.com"):
        
        self.qr_img = gen_qrcode(qrstr)
        self.image2.setPixmap(QPixmap.fromImage(ImageQt.toqimage(self.qr_img)))        

        
    def onClickedGen(self, evt):
        
        qrstr = self.txt_edit1.text()
        if qrstr:
            self.genQrcode(self.txt_edit1.text())
            #QMessageBox.information(self, "温馨提示", "生成二维码成功！")
            
        else:
            QMessageBox.warning(self, "警告提示", "请先输入要生成二维码的信息内容！")
    
    def onClickedSave(self, evt):
    
        if self.qr_img != None:           
            #获取当前时间,转化成字符串
            timenow = datetime.datetime.now()
            timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
            
            #保存二维码图片
            if not os.path.exists("imgs"):
                os.makedirs("imgs")
                
            filename = "imgs/qrcode-" + timestr + '.png'            
            self.qr_img.save(filename)
            #QMessageBox.information(self, "温馨提示", "保存二维码成功！")
            
        else:         
            QMessageBox.warning(self, "警告提示", "请先生成二维码！")
            


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    frame = GenQrcodeFrame()
    frame.show()
    
    code = app.exec_()
    sys.exit(code)