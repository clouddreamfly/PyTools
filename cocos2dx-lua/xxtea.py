#!/usr/bin/python
#-*-coding:utf8-*-



############################################################     
#                                                          #     
# The implementation of PHPRPC Protocol 3.0                #     
#                                                          #     
# xxtea.py                                                 #     
#                                                          #     
# Release 3.0.0                                            #     
# Copyright (c) 2005-2008 by Team-PHPRPC                   #     
#                                                          #     
# WebSite:  http://www.phprpc.org/                         #     
#           http://www.phprpc.net/                         #     
#           http://www.phprpc.com/                         #     
#           http://sourceforge.net/projects/php-rpc/       #     
#                                                          #     
# Authors:  Ma Bingyao <andot@ujn.edu.cn>                  #     
#                                                          #     
# This file may be distributed and/or modified under the   #     
# terms of the GNU Lesser General Public License (LGPL)    #     
# version 3.0 as published by the Free Software Foundation #     
# and appearing in the included file LICENSE.              #     
#                                                          #     
############################################################     
#     
# XXTEA encryption arithmetic library.     
#     
# Copyright (C) 2005-2008 Ma Bingyao <andot@ujn.edu.cn>     
# Version: 1.0     
# LastModified: Oct 5, 2008     
# This library is free.  You can redistribute it and/or modify it.     

import os
import sys
import fnmatch
import sitecustomize
import struct     

_DELTA = 0x9E3779B9     

def _long2str(v, w):     
    
    n = (len(v) - 1) << 2     
    if w:     
        m = v[-1]     
        if (m < n - 3) or (m > n): return ''     
        n = m     
    s = struct.pack('<%iL' % len(v), *v)    
    return s[0:n] if w else s     

def _str2long(s, w):     
    
    n = len(s)     
    m = (4 - (n & 3) & 3) + n     
    s = s.ljust(m, "\0")     
    v = list(struct.unpack('<%iL' % (m >> 2), s))     
    if w: v.append(n)     
    return v     

def encrypt(str, key):   
    
    if str == '': return str     
    v = _str2long(str, True)     
    k = _str2long(key.ljust(16, "\0"), False)     
    n = len(v) - 1     
    z = v[n]     
    y = v[0]     
    sum = 0     
    q = 6 + 52 // (n + 1)     
    while q > 0:     
        sum = (sum + _DELTA) & 0xffffffff     
        e = sum >> 2 & 3     
        for p in xrange(n):     
            y = v[p + 1]     
            v[p] = (v[p] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff     
            z = v[p]     
        y = v[0]     
        v[n] = (v[n] + ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[n & 3 ^ e] ^ z))) & 0xffffffff     
        z = v[n]     
        q -= 1     
    return _long2str(v, False)     

def decrypt(str, key):     
    
    if str == '': return str     
    v = _str2long(str, False)     
    k = _str2long(key.ljust(16, "\0"), False)     
    n = len(v) - 1     
    z = v[n]     
    y = v[0]     
    q = 6 + 52 // (n + 1)     
    sum = (q * _DELTA) & 0xffffffff     
    while (sum != 0):     
        e = sum >> 2 & 3     
        for p in xrange(n, 0, -1):     
            z = v[p - 1]     
            v[p] = (v[p] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[p & 3 ^ e] ^ z))) & 0xffffffff     
            y = v[p]     
        z = v[n]     
        v[0] = (v[0] - ((z >> 5 ^ y << 2) + (y >> 3 ^ z << 4) ^ (sum ^ y) + (k[0 & 3 ^ e] ^ z))) & 0xffffffff     
        y = v[0]     
        sum = (sum - _DELTA) & 0xffffffff     
    return _long2str(v, True)     



def ReadFile(filePath):
    file_object = open(filePath,'rb')
    all_the_text = file_object.read()
    file_object.close()
    return all_the_text

def WriteFile(filePath, all_the_text):    
    file_object = open(filePath,'wb')    
    file_object.write(all_the_text)
    file_object.close()

def BakFile(filePath, all_the_text):
    file_bak = filePath[:len(filePath)-3] + 'bak'
    WriteFile(file_bak, all_the_text)
    
    
def batch_encrypt(src_path, dest_path, sign, key, filterext = ".lua", fileext = '', appendext = False):
    
    for dirpath, dirnames, filenames in os.walk(src_path): 

        dest_dir = '.' + dirpath[len(src_path):]
        new_dest_path = os.path.join(dest_path, dest_dir)
        
        for filename in filenames:
            
            if os.path.splitext(filename)[1] == filterext or fnmatch.fnmatch(filename,filterext):  
            
                file_path = os.path.join(dirpath, filename)   
                print 'encrypt: %s'%(file_path)
                content = ReadFile(file_path)
        
                encrypt_content = encrypt(content, key)
                if len(sign) > 0: encrypt_content = sign + encrypt_content
                
                new_filename = ''
                if len(fileext) > 0 and appendext == False:
                    new_filename = os.path.splitext(filename)[0] + fileext
                elif len(fileext) > 0 and appendext == True:
                    new_filename = filename + fileext
                else:
                    new_filename = filename
                    
                if not os.path.exists(new_dest_path): os.makedirs(new_dest_path)
                new_file_path = os.path.join(new_dest_path, new_filename)                
                WriteFile(new_file_path, encrypt_content)
                
                

def batch_decrypt(src_path, dest_path, sign, key, filterext = ".luac", fileext = '', appendext = False):
    
    for dirpath, dirnames, filenames in os.walk(src_path): 
 
        dest_dir = '.' + dirpath[len(src_path):]
        new_dest_path = os.path.join(dest_path, dest_dir)
        
        for filename in filenames:
            
            if os.path.splitext(filename)[1] == filterext or fnmatch.fnmatch(filename,filterext):  
                
                file_path = os.path.join(dirpath, filename)
                #print 'decrypt: %s'%(file_path)
                content = ReadFile(file_path)
                
                if sign and len(sign) > 0:
                    if sign <> content[0:len(sign)]: continue
                    content = content[len(sign):]
                
                decrypt_content = decrypt(content, key)
                
                new_filename = ''
                if len(fileext) > 0 and appendext == False:
                    new_filename = os.path.splitext(filename)[0] + fileext
                elif len(fileext) > 0 and appendext == True:
                    new_filename = filename + fileext
                else:
                    new_filename = filename
                print 'decrypt: %s'%(file_path)    
                if not os.path.exists(new_dest_path): os.makedirs(new_dest_path)
                new_file_path = os.path.join(new_dest_path, new_filename)
                WriteFile(new_file_path, decrypt_content)         
                


if __name__ == "__main__":     
    
    sign = 'RY_QP_2016'
    key = 'RY_QP_MBCLIENT_!2016'
    src_path = r'assets/base'
    dest_path = r'assets2/base'
    filter_ext = '*.lua'
    file_ext = '.lua'
    
    print 'start decrypt........................'
    #batch_encrypt('as', 'ad', 'ss', 'key')
    batch_decrypt(src_path, dest_path, sign, key, filter_ext, file_ext)
    print 'decrypt finish........................'

