#!/usr/bin/python3
#-*-coding:utf-8-*-
  

import hashlib  
B16 = '0123456789ABCDEF'  
B30 = '123456789ABCDEFGHJKLMNPQRTVWXY'  
LicenseID='CNYKD-KALJK-JKKFV-WPHXT'  
RequestCode='RW711-RGGV3-T966R-HVNPA'  



def B(n,f,t):  
  xx = 0  
  for d in str(n):  
    xx = xx * len(f) + f.index(d)  
  res = ''  
  while xx > 0:  
    res=t[int(xx%len(t))]+res  
    xx//=len(t)  
  return res  


def S(D):  
  r = B(''.join([c for i,c in enumerate(D) if i//2*2==i]),B16,B30)  
  while len(r) < 17:  
    r = '1' + r  
  return r  


def A(c):  
  return c[:5]+'-'+c[5:10]+'-'+c[10:15]+'-'+c[15:]  


h = hashlib.sha1()  
h.update(RequestCode.encode('utf-8')+LicenseID.encode('utf-8'))  
lichash=A(RequestCode[:3]+S(h.hexdigest().upper()) )  
#data=[23,161,47,9] #6
#data=[221,13,93,27] #7
data=[179,95,45,245] #8

tmp=0  
realcode=''  
for i in data:  
  for j in lichash:  
    tmp=(tmp*i+ord(j))&0xFFFFF  
  realcode+=format(tmp,'=05X')  
  tmp=0  
  
D=B(realcode,B16,B30)  
while len(D) < 17:  
  D = '1' + D  
print("The Activation Code is: " +A('AXX'+D))

