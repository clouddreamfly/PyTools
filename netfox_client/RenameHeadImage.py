#!/user/bin/python
#-*-coding:utf8-*-



import os
import sys
import math
import random
import shutil
import fnmatch


# 重命名头像
def RenameHeadImage(path, old_str = "ffhyface", new_str = "dpokface", filterext = "*.jpg"):
    
    for dirpath, dirnames, filenames in os.walk(path): 
        
        for filename in filenames:
            
            if fnmatch.fnmatch(filename, filterext): 
                
                new_file_name = filename.replace(old_str, new_str)
                
                old_file_path = os.path.join(dirpath, filename)
                new_file_path = os.path.join(dirpath, new_file_name)

                print new_file_path
                os.rename(old_file_path, new_file_path)            
    



if __name__ == "__main__":
    
    RenameHeadImage(os.path.dirname(sys.argv[0])+ "\\dpok", old_str = "dpokface", new_str = "dqokface")
