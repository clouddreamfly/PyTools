#!/usr/bin/python3
#-*-encoding:utf8-*-

import os
import sys
import time
import tinify


tinify.key = "hjGXXVDM3QSfy9hrV6tFSdCYMHhjyxqD"


def searchFiles(path, ext):
    
   filepaths = []
   for dirpath, dirnames, filenames in os.walk(path):
      for dirname in dirnames:
         pass
         
      for filename in filenames:
         if str.lower(os.path.splitext(filename)[1]) == ext:
            filepath = os.path.join(dirpath, filename)
            filepaths.append(filepath)
            print(filepath)
    
   return filepaths


def compressImage(filepaths):
   for filepath in filepaths:
      before_size = os.stat(filepath).st_size
      start_time = time.time()
      source = tinify.from_file(filepath)
      source.to_file(filepath)
      after_size = os.stat(filepath).st_size
      print(filepath, "compress:", before_size, "->", after_size, "use time:", time.time() - start_time)


if __name__ == "__main__":
   print("start...")
   filepaths = searchFiles(r"D:\Workspace\image", ".png")
   compressImage(filepaths)
   print("finish...")

   



