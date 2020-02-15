import sys
from cx_Freeze import setup, Executable
 
build_exe_options = {"optimize": 2}
base = 'console'
 
if sys.platform == 'win64':
	base = 'Win64GUI'
 
executables = [
Executable(
	script='HttpDownload.py',
	base=base,
	targetName="HttpDownload.exe"
	)
]
 
setup(
	name='HttpDownload',
	version='0.1',
	description='Sample cx_Freeze script',
	options = {"build_exe": build_exe_options},
	executables=executables)