#!/user/bin/python
#-*-coding:utf8-*-


import os
import sys  
import time  
import math
import random
import requests  



#使用高德API
def geocodeGA(address):
   par = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
   base = 'http://restapi.amap.com/v3/geocode/geo'
   response = requests.get(base, par)
   answer = response.json()
   GPS=answer['geocodes'][0]['location'].split(",")
   return GPS[0],GPS[1]

#使用百度API
#key=f247cdb592eb43ebac6ccd27f796e2d2  DVa8ozBaZiDiCghUlOaVGh0fuly5CvdZ
def geocodeBA(address):
   base = 'http://api.map.baidu.com/geocoder/v2/?address='+ address + '&output=json&ak=DVa8ozBaZiDiCghUlOaVGh0fuly5CvdZ'
   response = requests.get(base)
   answer = response.json()
   print answer['message']
   return answer['result']['location']['lng'],answer['result']['location']['lat']

#使用百度API
#key=f247cdb592eb43ebac6ccd27f796e2d2  DVa8ozBaZiDiCghUlOaVGh0fuly5CvdZ
def geocodeBL(location):
   base = 'http://api.map.baidu.com/geocoder/v2/?location='+ location + '&output=json&ak=DVa8ozBaZiDiCghUlOaVGh0fuly5CvdZ'
   response = requests.get(base)
   answer = response.json()
   print answer['message']
   return answer['result']['location']['lng'],answer['result']['location']['lat']

#利用高德地图api实现经纬度与地址的批量转换 
#key=cb649a25c1f81c1451adbeca73623251
#key=7ec25a9c6716bb26f0d25e9fdfa012b8
#key=608d75903d29ad471362f8c58c550daf  

def transformGL(location):  
   parameters = {'coordsys':'gps','locations': location, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}  
   base = 'http://restapi.amap.com/v3/assistant/coordinate/convert'  
   response = requests.get(base, parameters)  
   answer = response.json()  
   print answer
   return answer['locations']

#利用高德地图
def geocodeGL(location):  
   parameters = {'location': location, 'radius': 3000, 'key': '7ec25a9c6716bb26f0d25e9fdfa012b8'}  
   base = 'http://restapi.amap.com/v3/geocode/regeo'  
   response = requests.get(base, parameters)  
   answer = response.json()  
   print answer
   return answer['regeocode']['formatted_address'], answer['regeocode']['addressComponent']





# 获取定位信息
def GetMapInfo(x, y, x1, x2, y1, y2, count, save_path = "addr_info.txt"):
   
   addr_info = []
   fp = open(save_path, 'a')
   
   for i in range(count):

      xx = x + random.triangular(x1, x2)
      yy = y + random.triangular(y1, y2)
      location = "%.6f,%.6f" %(xx, yy)
      
      time.sleep(0.2)
      
      try:
         detail, address = geocodeGL(transformGL(location))  
         print detail
         
         address_info = "%.6f#%.6f"%(xx, yy) + "#" + address["city"] + "#" + address["district"] 
         if len(address["township"]) > 0: address_info += ("#" + address["township"])
         if len(address["streetNumber"]["street"]) > 0: address_info += address["streetNumber"]["street"]
         else:
            if len(address["township"]) > 0:
               address_info += detail[detail.index(address["township"])+len(address["township"]):]
            else:
               address_info += ("#" + detail[detail.index(address["district"])+len(address["district"]):])
               
         print address_info
         addr_info.append(address_info)
         fp.write(address_info.encode("gbk")) 
         fp.write("\n")
         fp.flush()
      except:
         print "error!"
      
   fp.close()
   
   return addr_info

# 随机合成用户信息
def RandMerageUserInfo(ip_info, addr_info_path, user_name_path, save_path):
    
   if len(ip_info) == 0:
      return
   
   fp = open(save_path, 'w')
   fp2 = open(user_name_path, 'r')
   fp3 = open(addr_info_path, 'r')
   
   user_info = []
   addr_info = []
   addr_count = 0
   
   for user_name in fp2.readlines():
      user_name = user_name.replace('\n', '')   
      user_info.append(user_name)
   
   for addr in fp3.readlines():
      addr = addr.replace('\n', '')
      addr_info.append(addr)

   fp3.close()
   fp2.close()
   
   if len(addr_info) == 0:
      return
   
   random.shuffle(user_info)  
   for user_name in user_info:
      
      ip = ip_info[random.randint(0, len(ip_info)-1)].split(".")
      ip = ip[0] + "." + ip[1]  + "." + ip[2] + "." + str(random.randint(1, 255))
      addr = ""
      
      if addr_count < len(addr_info):
         addr = addr_info[addr_count]
         addr_count += 1
      else:
         addr = addr_info[random.randint(0, len(addr_info)-1)]
         addr_count += 1
      
      one_user_info = user_name + "  &&&&  " + ip +"#" + addr + "  &&&&  " + ip + "\n" 
      fp.write(one_user_info)
   
   fp.close()
   
   
def RandMerageUserInfo2(ip_info, addr_info, user_name_path, save_path):
   
   if len(ip_info) == 0 or len(addr_info) == 0:
      return
   
   fp = open(save_path, 'w')
   fp2 = open(user_name_path, 'r')
   
   user_info = []
   addr_count = 0
   
   for user_name in fp2.readlines():
      user_name = user_name.replace('\n', '')   
      user_info.append(user_name)

   fp2.close()
   
   random.shuffle(user_info)
   for user_name in user_info:
      
      ip = ip_info[random.randint(0, len(ip_info)-1)].split(".")
      ip = ip[0] + "." + ip[1]  + "." + ip[2] + "." + str(random.randint(1, 255))
      addr = ""
      
      if addr_count < len(addr_info):
         addr = addr_info[addr_count]
         addr_count += 1
      else:
         addr = addr_info[random.randint(0, len(addr_info)-1)]
         addr_count += 1
      
      one_user_info = user_name + "  &&&&  " + ip +"#" + addr.encode(encoding='gbk') + "  &&&&  " + ip + "\n" 
      fp.write(one_user_info)
   
   fp.close()
   
  
def RandUserInfo(user_name_path, save_path):
      
   fp = open(save_path, 'w')
   fp2 = open(user_name_path, 'r')
   
   user_info = []

   
   for user_name in fp2.readlines():
      user_name = user_name.replace('\n', '')   
      user_info.append(user_name)

   fp2.close()
   
   random.shuffle(user_info)
   for user_name in user_info:
      one_user_info = user_name + "\n" 
      fp.write(one_user_info)
   
   fp.close()
   
   
#def RandUserInfo_KeShan():


   #fp = open("UserInfoKeShan.txt", 'w')
   #fp2 = open("10000ID.txt", 'r')

   #for index in range(0, 1):

      #info = MapInfo[random.randint(0, len(MapInfo)-1)]
      #user_name = fp2.readline().replace('\n', '')
      #x = float("%.6f" % (info["x"] + random.triangular(0.0, 0.09)))
      #y = float("%.6f" % (info["y"] + random.triangular(0.0, 0.09)))
      #ip = info["ip"].split(".")
      #ip = ip[0] + "." + ip[1]  + "." + ip[2] + "." + str(random.randint(1, 255))
      #user_info = user_name + "  &&&&  " + ip +"#" + str(x) + "#" + str(y) + "#" + info["addr"].encode(encoding='gbk') + "  &&&&  " + ip + "\n" 
      #fp.write(user_info)

   #fp2.close()
   #fp.close()



   
# 
ip_info1 = [
      "61.53.212.3",
       "61.53.212.32",
       "61.53.212.41",
       "61.53.212.49",
       "61.53.212.72",
       "221.15.2.116",
       "221.15.2.200",
       "221.15.2.55",
       "221.15.2.43",
       "222.140.149.166",
       "222.140.149.170",
       "222.140.149.180",
       "221.15.2.33",
       "221.15.2.29",
       "221.15.2.28",
       "61.54.149.110",
       "61.54.149.100",
       "61.54.149.15"
   ]
   
# 克山
ip_info2 = [
   "61.167.65.98",
   "61.167.65.14",
   "61.158.76.75",
   "61.138.42.90",
   "1.60.192.0",
   "1.191.8.0",
   "1.191.0.0",
   "1.57.89.0",
   "1.57.101.0",
   "1.57.107.0",
   "42.185.100.0",
   "42.185.129.0",
   "42.101.255.44",
   "113.5.2.30",
   "1.60.195.0",
   "42.102.210.203",
   "117.179.117.196",
   "1.61.161.0",	
   "1.61.165.0",	
   "60.14.44.0",	
   "112.101.9.0",
   "113.8.19.0",	
   "122.157.128.0",
   "211.93.55.187",
   "218.10.5.199",	
   "221.209.46.246",
   "42.102.16.79",
   "117.136.7.125",
   "42.102.16.79",
   "123.165.247.19",
   "111.43.251.134"   
]


# 龙江
ip_info3 = [
   "113.5.2.37",
   "113.5.4.127",
   "1.191.11.6",
   "10.63.78.127",
   "113.5.6.47",
   "10.62.78.106",
   "1.191.12.18",
   "10.63.72.120",
   "113.5.2.220"
]

# 大庆
ip_info4 = [
   "221.209.217.141",
   "218.9.4.9",
   "112.101.97.203", 
   "112.101.97.63",
   "221.209.170.199", 
   "114.196.16.190", 
   "122.156.203.220", 
   "221.209.137.238", 
   "122.156.210.124", 
   "61.167.201.87",
   "112.101.108.178",  
   "221.209.183.101", 
   "122.158.36.164",
   "112.101.116.155", 
   "60.218.91.231", 
   "112.101.117.236",  
   "1.59.43.122", 
   "112.101.102.58",  
   "113.5.2.65", 
   "60.252.33.36", 
   "60.252.41.57", 
   "223.104.17.207",
   "114.196.22.160", 
   "112.98.125.132", 
   "60.252.145.54",  
   "122.158.16.49",  
   "60.218.169.42", 
   "113.5.2.2", 
   "112.101.97.37",  
   "223.104.17.122"  
]


#龙岩
ip_info5 = [
   "218.6.43.14",	
   "218.6.43.21",	
   "218.6.43.5",	
   "58.22.226.162",	
   "218.86.103.208",	
   "220.162.113.218",	
   "220.162.113.217",	
   "218.6.38.236",	
   "220.162.159.111",	
   "220.162.159.108",	
   "218.6.38.223",	
   "220.162.159.106",	
   "218.86.97.120",	
   "218.86.101.12",	
   "218.86.101.22",	
   "218.86.101.16",	
   "220.200.12.207",	
   "218.6.43.15",	
   "218.86.101.18",	
   "218.86.101.20",	
   "218.6.43.18",	
   "218.86.101.25",	
   "218.86.101.14",	
   "218.86.101.24",	
   "218.86.101.23",	
   "218.6.43.3",	
   "222.78.72.86",	
   "218.6.43.23",	
   "218.86.101.3",	
   "220.162.113.143",	
   "218.6.38.233",	
   "218.6.38.207",	
   "220.162.163.106",	
   "220.162.159.132",	
   "220.162.159.205",	
   "218.6.31.138",	
   "218.6.31.150",	
   "220.162.159.138",	
   "218.6.35.198",	
   "220.162.103.9",	
   "218.6.35.169",	
   "218.6.35.159",	
   "218.86.101.27",	
   "218.6.37.3",	
   "218.6.38.197",	
   "220.162.157.131",	
   "220.162.158.222",	
   "218.86.101.118",	
   "220.162.157.145",	
   "211.138.140.163",	
   "220.162.113.195",	
   "218.6.43.13",	
   "218.6.38.226",	
   "218.6.38.224",	
   "218.6.38.225",	
   "220.162.117.82",	
   "218.86.92.12",	
   "218.6.35.140",	
   "218.6.31.139",	
   "220.162.159.69",	
   "218.86.103.67",	
   "218.6.43.50",	
   "220.162.157.144",	
   "220.162.145.70",	
   "220.162.144.134",	
   "59.58.224.93",	
   "220.162.144.195",	
   "117.27.113.113",	
   "218.86.97.11",	
   "220.162.145.72",	
   "220.162.145.73",	
   "220.162.145.78",	
   "218.86.97.3",	
   "220.162.157.150",	
   "220.162.160.8",	
   "218.6.35.193",	
   "220.162.159.255",	
   "220.162.159.199",	
   "218.6.31.134",	
   "218.6.38.228",	
   "220.162.113.199",	
   "222.78.104.97",	
   "220.162.113.200",	
   "61.154.57.50",	
   "218.86.101.13",	
   "218.6.43.46",	
   "218.6.43.16",	
   "218.86.95.129",	
   "220.162.160.2",	
   "220.162.113.221",	
   "220.162.113.216",	
   "220.162.113.204",	
   "220.162.163.105",	
   "220.162.157.151",	
   "220.162.160.133",	
   "220.162.159.34",	
   "220.162.163.194",	
   "220.162.163.66",	
   "218.6.31.135",	
   "218.6.31.132",	
   "220.162.159.135",	
   "218.86.97.175",	
   "218.86.86.60",	
   "218.86.96.8",	
   "220.162.157.68",	
   "218.6.43.143",	
   "218.6.37.47",	
   "218.86.96.68",	
   "218.6.43.154",	
   "218.86.97.176",	
   "218.86.97.178",	
   "220.162.159.66",	
   "218.6.38.230",	
   "218.6.38.254",	
   "218.6.43.200",	
   "218.6.43.60",	
   "220.162.157.169",	
   "218.86.101.123",	
   "218.86.101.110",	
   "218.6.43.20",	
   "220.162.158.40",	
   "218.86.94.104",	
   "220.200.12.221",	
   "59.60.179.237",	
   "218.6.35.156",	
   "220.162.159.103",	
   "220.162.159.139",	
   "220.162.145.6",	
   "218.86.103.155",	
   "220.162.145.77",	
   "222.78.87.107",	
   "222.78.91.76",	
   "218.86.97.119",	
   "218.86.97.38",	
   "218.86.103.137",	
   "218.6.35.129",	
   "218.6.38.208",	
   "220.162.163.162",	
   "220.162.163.101",	
   "218.86.103.41",	
   "220.162.163.99",	
   "220.162.163.98",	
   "220.162.163.100",	
   "220.162.163.102",	
   "218.86.103.49",	
   "220.162.159.68",	
   "220.162.161.100",	
   "220.162.161.223",	
   "218.6.43.243",	
   "218.86.97.36",	
   "218.6.43.227",	
   "218.86.97.60",	
   "218.86.97.59",	
   "218.6.43.196",	
   "222.78.93.104",	
   "59.58.200.202",	
   "218.86.97.46",	
   "218.86.97.39",	
   "218.6.43.201",	
   "120.34.70.97",	
   "218.6.38.93",	
   "220.162.145.16",	
   "218.6.38.87",	
   "218.6.38.113",	
   "218.6.36.209",	
   "218.6.38.114",	
   "218.6.38.86",	
   "218.86.103.231",	
   "218.6.38.94",	
   "218.6.38.85",	
   "218.6.38.101",	
   "218.6.38.92",	
   "218.86.103.230",	
   "220.162.113.15",	
   "218.6.38.88",	
   "218.6.38.108",	
   "218.6.43.4",	
   "220.162.158.7",	
   "220.162.158.3",	
   "218.6.43.11",	
   "218.6.43.63",	
   "220.162.158.8",	
   "220.162.158.187",	
   "218.86.97.201",	
   "218.86.97.199",	
   "218.86.101.136",	
   "218.86.97.115",	
   "220.162.157.167",	
   "220.162.159.67",	
   "220.162.163.134",	
   "220.162.159.74",	
   "220.162.158.139",	
   "220.162.163.70",	
   "222.78.65.37",	
   "220.162.163.67",	
   "220.162.163.136",	
   "220.162.157.186",	
   "222.78.76.192",	
   "220.162.163.103",	
   "220.162.113.222",	
   "220.162.159.227",	
   "220.162.163.69",	
   "220.162.110.37",	
   "218.6.35.168",	
   "220.162.159.104",	
   "220.200.12.254",	
   "222.78.65.41",	
   "220.162.158.137",	
   "222.78.65.39",	
   "220.162.145.204",	
   "218.6.38.26",	
   "220.162.103.201",	
   "59.58.206.166",	
   "220.162.103.199",	
   "218.6.39.234",	
   "218.86.103.182",	
   "218.86.97.227",	
   "218.86.97.229",	
   "218.86.103.167",	
   "218.86.103.176",	
   "218.86.103.151",	
   "218.86.103.171",	
   "218.86.103.136",	
   "220.162.103.165",	
   "218.86.97.231",	
   "222.78.80.191",	
   "61.154.59.105",	
   "220.162.103.200",	
   "218.6.38.50",	
   "218.6.38.16",	
   "59.58.206.145",	
   "220.162.103.39",	
   "220.162.103.197",	
   "220.162.103.164",	
   "218.6.38.176",	
   "218.86.102.29",	
   "218.6.38.153",	
   "218.86.102.10",	
   "220.162.102.105",	
   "218.86.102.20",	
   "218.6.38.155",	
   "218.86.102.12",	
   "220.162.102.21",	
   "220.162.102.5",	
   "218.6.38.149",	
   "218.86.102.7",	
   "218.86.102.6",	
   "218.6.38.181",	
   "218.86.102.32",	
   "220.162.133.111",	
   "220.162.102.4",	
   "218.6.38.158",	
   "218.86.102.8",	
   "218.86.102.19",	
   "218.86.102.28"   
]

if __name__=="__main__":
   
   ##
   #x = 114
   #y = 32
   #x1 = 0.0600000001 
   #x2 = 0.1900000009
   #y1 = 0.0000000001
   #y2 = 0.10000000009
   #count = 2000
   #save_path = "addr_info1.txt"
   
   #addr_info = GetMapInfo(x, y, x1, x2, y1, y2, count, save_path)
   ##RandMerageUserInfo2(ip_info1, addr_info, "10000ID.txt", "UserInfo_XinYang.txt")
   #RandMerageUserInfo(ip_info1, save_path, "10000ID.txt", "UserInfo_XinYang.txt")
   
   ## 克山
   #x = 125 
   #y = 48 
   #x1 = 0.00002
   #x2 = 0.99999
   #y1 = 0.00101
   #y2 = 0.26999
   #count = 8
   #save_path="addr_info2.txt"
   
   #addr_info = GetMapInfo(x, y, x1, x2, y1, y2, count, save_path)
   ##RandMerageUserInfo2(ip_info2, addr_info, "10000ID.txt", "UserInfo_keShang.txt")
   #RandMerageUserInfo(ip_info2, save_path, "10000ID.txt", "UserInfo_keShang.txt")
   
   ## 龙江
   #x = 122 
   #y = 47 
   #x1 = 0.60002025562232
   #x2 = 1.69999012652112
   #y1 = 0.001010010001124
   #y2 = 0.450999030005555
   #count = 1
   #save_path="addr_info3.txt"
   
   #addr_info = GetMapInfo(x, y, x1, x2, y1, y2, count, save_path)
   ##RandMerageUserInfo2(ip_info3, addr_info, "10000ID.txt", "UserInfo_LongJiang.txt")
   #RandMerageUserInfo(ip_info3, save_path, "10000ID.txt", "UserInfo_LongJiang.txt")   
   
   ## 大庆
   #x = 124
   #y = 46
   #x1 = 0.7030700000232
   #x2 = 1.200000000652112
   #y1 = 0.20000000001124
   #y2 = 0.500999030005555
   #count = 1
   #save_path="addr_info4.txt"
   
   #addr_info = GetMapInfo(x, y, x1, x2, y1, y2, count, save_path)
   ##RandMerageUserInfo2(ip_info4, addr_info, "10000ID.txt", "UserInfo_DaQing.txt")
   #RandMerageUserInfo(ip_info4, save_path, "10000ID.txt", "UserInfo_DaQing.txt")      
   
   
   #x = 117
   #y = 25
   #x1 = -0.4030700000232
   #x2 = 0.400000000652112
   #y1 = -0.20000000001124
   #y2 = 0.300999030005555
   #count = 1
   #save_path="addr_info5.txt"
   #
   #addr_info = GetMapInfo(x, y, x1, x2, y1, y2, count, save_path)
   ##RandMerageUserInfo2(ip_info5, addr_info, "10000ID.txt", "UserInfo_LongYan.txt")
   #RandMerageUserInfo(ip_info5, save_path, "10000ID.txt", "UserInfo_LongYan.txt")    

   RandUserInfo("10000ID.txt", "UserInfo_shanxi.txt")     
   
   
   print "finish......."


