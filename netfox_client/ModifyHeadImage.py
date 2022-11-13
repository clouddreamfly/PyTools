#!/user/bin/python
#-*-coding:utf8-*-



import os
import sys
import math
import random
import shutil
import fnmatch


# 修改头像
def ModifyHeadImageName(path, save_path, image_index = 1, head_image_str = "ffhyface", filterext = "*.jpg"):
    
    for filename in os.listdir(path): 
        
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path) :
            ModifyHeadImageName(file_path, save_path, image_index, head_image_str, filterext)
        else:
            
            file_ext = os.path.splitext(filename)[1]
            if fnmatch.fnmatch(filename,filterext):  
                new_file_name = head_image_str + str(image_index) + file_ext
                new_file_path = os.path.join(path, "..\\" + save_path + "\\" + new_file_name)
                image_index += 1
                print new_file_path
                shutil.copyfile(file_path, new_file_path)


if __name__ == "__main__":
    
    ModifyHeadImageName(os.path.dirname(sys.argv[0])+ "\\headImage", "save")