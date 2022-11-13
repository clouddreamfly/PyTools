
#!/usr/bin/python
#-*-coding=utf8-*-


import os
import sys
import fnmatch
import sitecustomize



def search_file(search_path, filterext = "*.sql"):
    
    for dirpath, dirnames, filenames in os.walk(search_path): 
        
        for filename in filenames:
            
            if fnmatch.fnmatch(filename, filterext):  
  
                print u"osql -S %%serverName%% -U %%username%% -P %%password%% -i \"%%rootPath%%%s\""%(filename)
                
                
                
                
if __name__ == '__main__':  
 
    search_path = r"辅助脚本\金币数据库"
    search_file(search_path)