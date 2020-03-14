#!/usr/bin/env python
# encoding:utf-8

from socket import  *
from ctypes import create_string_buffer
from struct import *
import sysconfig
import random
from ctypes.wintypes import BYTE
from msilib import datasizemask
from _ctypes import sizeof
from random import randint
from time import sleep
import threading
import select

CODEC = 'utf-8'


'''-----------------Packet_struct--------------------------------------------'''

#//////////////////////////////////////////////////////////////////////////////////
#数据定义

#"网络数据定义"
SOCKET_VER = 0x66    #"#网络版本"  ida_pro 逆向找到EncryptBuffer函数后可以确定此值
DWORD_SIZE= 4
WORD_SIZE = 2
BYTE_SIZE = 1
HEAD_SIZE = 4
CMD_SIZE = 4

#数据类型
DK_MAPPED	= 0x01		#映射类型
DK_ENCRYPT	= 0x02		#加密类型
DK_COMPRESS	= 0x04		#压缩类型

#长度定义
SOCKET_TCP_BUFFER = 8192				   #网络缓冲
SOCKET_TCP_HEAD = 8				           #网络头部
SOCKET_TCP_PACKET = (SOCKET_TCP_BUFFER - SOCKET_TCP_HEAD)  #网络缓冲
SOCKET_TCP_DATA	  = (SOCKET_TCP_PACKET - 64)		   #网络数据



#加密密钥
g_dwPacketKey=0xA55AA55A

#发送映射
g_SendByteMap=(
	0x70, 0x2F, 0x40, 0x5F, 0x44, 0x8E, 0x6E, 0x45, 0x7E, 0xAB, 0x2C, 0x1F, 0xB4, 0xAC, 0x9D, 0x91,
	0x0D, 0x36, 0x9B, 0x0B, 0xD4, 0xC4, 0x39, 0x74, 0xBF, 0x23, 0x16, 0x14, 0x06, 0xEB, 0x04, 0x3E,
	0x12, 0x5C, 0x8B, 0xBC, 0x61, 0x63, 0xF6, 0xA5, 0xE1, 0x65, 0xD8, 0xF5, 0x5A, 0x07, 0xF0, 0x13,
	0xF2, 0x20, 0x6B, 0x4A, 0x24, 0x59, 0x89, 0x64, 0xD7, 0x42, 0x6A, 0x5E, 0x3D, 0x0A, 0x77, 0xE0,
	0x80, 0x27, 0xB8, 0xC5, 0x8C, 0x0E, 0xFA, 0x8A, 0xD5, 0x29, 0x56, 0x57, 0x6C, 0x53, 0x67, 0x41,
	0xE8, 0x00, 0x1A, 0xCE, 0x86, 0x83, 0xB0, 0x22, 0x28, 0x4D, 0x3F, 0x26, 0x46, 0x4F, 0x6F, 0x2B,
	0x72, 0x3A, 0xF1, 0x8D, 0x97, 0x95, 0x49, 0x84, 0xE5, 0xE3, 0x79, 0x8F, 0x51, 0x10, 0xA8, 0x82,
	0xC6, 0xDD, 0xFF, 0xFC, 0xE4, 0xCF, 0xB3, 0x09, 0x5D, 0xEA, 0x9C, 0x34, 0xF9, 0x17, 0x9F, 0xDA,
	0x87, 0xF8, 0x15, 0x05, 0x3C, 0xD3, 0xA4, 0x85, 0x2E, 0xFB, 0xEE, 0x47, 0x3B, 0xEF, 0x37, 0x7F,
	0x93, 0xAF, 0x69, 0x0C, 0x71, 0x31, 0xDE, 0x21, 0x75, 0xA0, 0xAA, 0xBA, 0x7C, 0x38, 0x02, 0xB7,
	0x81, 0x01, 0xFD, 0xE7, 0x1D, 0xCC, 0xCD, 0xBD, 0x1B, 0x7A, 0x2A, 0xAD, 0x66, 0xBE, 0x55, 0x33,
	0x03, 0xDB, 0x88, 0xB2, 0x1E, 0x4E, 0xB9, 0xE6, 0xC2, 0xF7, 0xCB, 0x7D, 0xC9, 0x62, 0xC3, 0xA6,
	0xDC, 0xA7, 0x50, 0xB5, 0x4B, 0x94, 0xC0, 0x92, 0x4C, 0x11, 0x5B, 0x78, 0xD9, 0xB1, 0xED, 0x19,
	0xE9, 0xA1, 0x1C, 0xB6, 0x32, 0x99, 0xA3, 0x76, 0x9E, 0x7B, 0x6D, 0x9A, 0x30, 0xD6, 0xA9, 0x25,
	0xC7, 0xAE, 0x96, 0x35, 0xD0, 0xBB, 0xD2, 0xC8, 0xA2, 0x08, 0xF3, 0xD1, 0x73, 0xF4, 0x48, 0x2D,
	0x90, 0xCA, 0xE2, 0x58, 0xC1, 0x18, 0x52, 0xFE, 0xDF, 0x68, 0x98, 0x54, 0xEC, 0x60, 0x43, 0x0F
)

#接收映射
g_RecvByteMap=(
	0x51, 0xA1, 0x9E, 0xB0, 0x1E, 0x83, 0x1C, 0x2D, 0xE9, 0x77, 0x3D, 0x13, 0x93, 0x10, 0x45, 0xFF,
	0x6D, 0xC9, 0x20, 0x2F, 0x1B, 0x82, 0x1A, 0x7D, 0xF5, 0xCF, 0x52, 0xA8, 0xD2, 0xA4, 0xB4, 0x0B,
	0x31, 0x97, 0x57, 0x19, 0x34, 0xDF, 0x5B, 0x41, 0x58, 0x49, 0xAA, 0x5F, 0x0A, 0xEF, 0x88, 0x01,
	0xDC, 0x95, 0xD4, 0xAF, 0x7B, 0xE3, 0x11, 0x8E, 0x9D, 0x16, 0x61, 0x8C, 0x84, 0x3C, 0x1F, 0x5A,
	0x02, 0x4F, 0x39, 0xFE, 0x04, 0x07, 0x5C, 0x8B, 0xEE, 0x66, 0x33, 0xC4, 0xC8, 0x59, 0xB5, 0x5D,
	0xC2, 0x6C, 0xF6, 0x4D, 0xFB, 0xAE, 0x4A, 0x4B, 0xF3, 0x35, 0x2C, 0xCA, 0x21, 0x78, 0x3B, 0x03,
	0xFD, 0x24, 0xBD, 0x25, 0x37, 0x29, 0xAC, 0x4E, 0xF9, 0x92, 0x3A, 0x32, 0x4C, 0xDA, 0x06, 0x5E,
	0x00, 0x94, 0x60, 0xEC, 0x17, 0x98, 0xD7, 0x3E, 0xCB, 0x6A, 0xA9, 0xD9, 0x9C, 0xBB, 0x08, 0x8F,
	0x40, 0xA0, 0x6F, 0x55, 0x67, 0x87, 0x54, 0x80, 0xB2, 0x36, 0x47, 0x22, 0x44, 0x63, 0x05, 0x6B,
	0xF0, 0x0F, 0xC7, 0x90, 0xC5, 0x65, 0xE2, 0x64, 0xFA, 0xD5, 0xDB, 0x12, 0x7A, 0x0E, 0xD8, 0x7E,
	0x99, 0xD1, 0xE8, 0xD6, 0x86, 0x27, 0xBF, 0xC1, 0x6E, 0xDE, 0x9A, 0x09, 0x0D, 0xAB, 0xE1, 0x91,
	0x56, 0xCD, 0xB3, 0x76, 0x0C, 0xC3, 0xD3, 0x9F, 0x42, 0xB6, 0x9B, 0xE5, 0x23, 0xA7, 0xAD, 0x18,
	0xC6, 0xF4, 0xB8, 0xBE, 0x15, 0x43, 0x70, 0xE0, 0xE7, 0xBC, 0xF1, 0xBA, 0xA5, 0xA6, 0x53, 0x75,
	0xE4, 0xEB, 0xE6, 0x85, 0x14, 0x48, 0xDD, 0x38, 0x2A, 0xCC, 0x7F, 0xB1, 0xC0, 0x71, 0x96, 0xF8,
	0x3F, 0x28, 0xF2, 0x69, 0x74, 0x68, 0xB7, 0xA3, 0x50, 0xD0, 0x79, 0x1D, 0xFC, 0xCE, 0x8A, 0x8D,
	0x2E, 0x62, 0x30, 0xEA, 0xED, 0x2B, 0x26, 0xB9, 0x81, 0x7C, 0x46, 0x89, 0x73, 0xA2, 0xF7, 0x72
)



class SocketClient(object):
    
    def __init__(self):
        
        self.m_Socket = None
        self.m_IsConnect = False
        self.m_wRecvSize = 0
        
        self.m_dwSendPacketCount = 0	#发送计数
        self.m_dwRecvPacketCount = 0	#接受计数        
        self.m_cbSendRound = 0  #发送字节映射
        self.m_cbRecvRound = 0  #接收字节映射
        self.m_dwSendXorKey = 0  #发送密钥
        self.m_dwRecvXorKey = 0 #接收密钥     
        
        self.m_cbCacheBuffer = create_string_buffer(SOCKET_TCP_BUFFER+DWORD_SIZE)
        
        
    def __del__(self):
        
        self.disconnect()
        
        
    def connect(self, socket_addr):
        
        try:
            self.m_Socket = socket(AF_INET, SOCK_STREAM)
            self.m_Socket.connect(socket_addr)
            self.m_IsConnect = True
        except:
            self.disconnect()
            return False
    
        return True      

    def disconnect(self):
        
        if self.m_Socket != None:
            self.m_Socket.close()
            self.m_Socket = None
            self.m_IsConnect = False
            
    def send_data(self, main_cmd, sub_cmd, data = None):
        
        if self.m_Socket == None or self.m_IsConnect == False:
            return False
        
        data_size = 0
        if data is not None: data_size = len(data)
        data_packet_size = SOCKET_TCP_HEAD + data_size
        data_buffer = create_string_buffer(data_packet_size)
        
        pack_into("B", data_buffer, 0, SOCKET_VER)
        pack_into("B", data_buffer, 1, 0)
        pack_into("H", data_buffer, 2, data_packet_size)
        pack_into("H", data_buffer, 4, main_cmd)
        pack_into("H", data_buffer, 6, sub_cmd)
        
        i = 0
        while i < data_size:
            pack_into("B", data_buffer, i + SOCKET_TCP_HEAD, data[i])
            i += 1
        
        send_size, send_data = self.EncryptBuffer(data_buffer, data_packet_size)
        if send_size > 0: 
            try:
                self.m_Socket.send(send_data[:send_size])
                return True
            except:
                return False
        
        return False
            
    def SeedRandMap(self, seed):
        
        num = int(seed)
        num = ( num * 241103 + 2533101 ) >> 16
        
        return ((num | int(0xFFFF0000)) - 0xFFFF0000) #返回一个WORD类型            
            
    def MapSendByte(self, byte):
  
        index = byte + self.m_cbSendRound
        b = g_SendByteMap[index % 0x100]
        self.m_cbSendRound += 3
        
        return b
    
    def MapRecvByte(self, byte):
  
        b = g_RecvByteMap[byte] - self.m_cbRecvRound
        b = b % 0x100
        self.m_cbRecvRound += 3
        
        return b
    

    def CrevasseBuffer(self, data_buffer, data_size):
        
        if self.m_dwSendPacketCount == 0 or data_size < SOCKET_TCP_HEAD :
            print "data error"
            return 0
        
        wEncryptSize = data_size - HEAD_SIZE
        wSnapCount = 0
        if (((data_size - HEAD_SIZE) % DWORD_SIZE ) != 0) :
            wSnapCount = DWORD_SIZE - wEncryptSize % DWORD_SIZE
   
        #解密数据        
        dwXorKey = self.m_dwRecvXorKey
        wEncrypCount = (wEncryptSize - wSnapCount) / DWORD_SIZE
        i = 0
        j = 4   #排除cmd_info,从CMD_Command起
        k = 4
        
        while i < wEncrypCount :
                
            wSeed = unpack_from("H", data_buffer, k)[0]
            k += 2
            dwXorKey = self.SeedRandMap(wSeed)
            dwXorKey |= int(self.SeedRandMap(unpack_from("H", data_buffer, k)[0]) ) << 16
            k += 2
            
            dwXorKey ^= g_dwPacketKey
            dwXorData = unpack_from("I", data_buffer, j)[0]
            dwXorData ^= self.m_dwRecvXorKey
            pack_into("I", data_buffer, j, dwXorData)
            j += 4
            self.m_dwRecvXorKey = dwXorKey
            i += 1
    
        i = 4
        cbCheckCode = unpack_from('B', data_buffer, 1)[0]
        while i < data_size:
            pack_into("B", data_buffer, i, self.MapRecvByte( ord(data_buffer[i]) ))
            cbCheckCode += ord(data_buffer[i])
            cbCheckCode = cbCheckCode % 0x100
            i += 1
            
        if cbCheckCode != 0:
            print "check code error:" , cbCheckCode
            raise "check code error"
            
        return data_size
    
    
    def EncryptBuffer(self, data_buffer, data_size):
        
        wEncryptSize = data_size - 4 #排除cmd_info4字节头不加密
        wSnapCount = 0
        if ((wEncryptSize % DWORD_SIZE) != 0): #待加密数据对齐粒度 4字节
            wSnapCount = DWORD_SIZE - (wEncryptSize % DWORD_SIZE)  #不足4字节补-0
            n = 0
            while n < wSnapCount:
                pack_into("B", data_buffer, data_size + n, 0x0)
                n += 1
    
        cbCheckCode = 0 #务必置0
        i = 4 #起始位置，排除CMD_INFO逐字节与发送映射表替换，并计算出校验和
        while i < data_size:
            cbCheckCode += ord(data_buffer[i])
            cbCheckCode = cbCheckCode % 0x100
            data = self.MapSendByte(ord(data_buffer[i]))
            pack_into("B", data_buffer, i, data)
            i += 1
    
        #填写计算出的校验码
        packet_size = data_size
        #pack_into ("B", data_buffer, 0, DK_ENCRYPT)
        pack_into ("B", data_buffer, 1, ( ~cbCheckCode + 1) % 0x100)
        pack_into ("H", data_buffer, 2, packet_size)
    
        dwXorKey = self.m_dwSendXorKey
        if ( self.m_dwSendPacketCount == 0 ):
            dwXorKey = random.randint(0x11111111, 0xeeeeeeee) #生成随机密钥
            dwXorKey ^= g_dwPacketKey
            m_dwSendXorKey = dwXorKey
            m_dwRecvXorKey = dwXorKey
    
    
        #加密数据
        i = 0
        j = 4   #排除cmd_info,从CMD_Command起
        k = 4
        wEncryptCount = (wEncryptSize + wSnapCount) / DWORD_SIZE
        while i < wEncryptCount:
            dwXorData =  unpack_from("I", data_buffer, j)[0]
            dwXorData ^= dwXorKey
            pack_into("I", data_buffer, j, dwXorData)
            j += 4 #逐4字节异或加密数据
            dwXorKey = self.SeedRandMap ( unpack_from ("H", data_buffer, k)[0])  #用加密后的数据加密生成新的密钥
            k += 2
            dwXorKey |= int( self.SeedRandMap( unpack_from ("H", data_buffer, k)[0])) << 16 #
            k += 2
            dwXorKey ^= g_dwPacketKey
            i += 1
    
        #插入密钥
        if (self.m_dwSendPacketCount == 0):
            i = 0
            while i < SOCKET_TCP_HEAD:
                pack_into("B", self.m_cbCacheBuffer, i, ord(data_buffer[i]))      #前八个字节相同
                i += 1
                
            packet_size = data_size + DWORD_SIZE #因为插入了4B的密钥
            pack_into("H", self.m_cbCacheBuffer, 2, packet_size)                
            pack_into("I", self.m_cbCacheBuffer, SOCKET_TCP_HEAD, m_dwSendXorKey)  #插入异或密钥key
            j = SOCKET_TCP_HEAD
            while j < data_size:
                pack_into("B", self.m_cbCacheBuffer, j + DWORD_SIZE, ord(data_buffer[j]) )
                j += 1
                
        else:
            i = 0
            while i < packet_size:
                pack_into("B", self.m_cbCacheBuffer, i, ord(data_buffer[i]))
                i += 1 
                 
        self.m_dwSendPacketCount += 1
        self.m_dwSendXorKey = dwXorKey      
        
        return packet_size, self.m_cbCacheBuffer
    




HOST = "172.16.1.110"
PORT = 9301
ADDR = (HOST, PORT)


def test_thread(event):

    cs = []
    dcs = {}
    fcs = {}
    for i in range(126):
        try:
            s = SocketClient()
            if s.connect(ADDR):
                s.send_data(0, 1)
                cs.append(s.m_Socket)
                dcs[s.m_Socket] = s
            else:
                print("socket connect fail\n")
                pass
        except:
            print("socket connect error\n")
   
    while event.isSet():
    
        if len(cs) == 0: break
        
        r_list, w_list, e_list = select.select(cs, cs, [], 1)
        for s in r_list:
            try:
                data = s.recv(1024)
                print("len=%d, data=%s\n"%(len(data), data))
            except:
                print("error\n")
                dcs[s].disconnect()
                cs.remove(s)
                fcs[s] = dcs[s]
                del dcs[s]
                
        for s in w_list:
            if dcs.has_key(s) : dcs[s].send_data(0, 1)
    
        sleep(3)
        
    print("thread quit\n")

    
if __name__ == "__main__":
    

    event_obj = threading.Event()#创建一个事件
    event_obj.set()
    for i in range(1):
        t = threading.Thread(target=test_thread, args=(event_obj,))
        t.start()

    data= raw_input(u'请输入要：')
    event_obj.clear()
    print(u"结束\n")
        

    
    
    