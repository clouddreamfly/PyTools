# A very simple setup script to create 2 executables.
#
# hello.py is a simple "hello, world" type program, which alse allows
# to explore the environment in which the script runs.
#
# test_wx.py is a simple wxPython program, it will be converted into a
# console-less program.
#
# If you don't have wxPython installed, you should comment out the
#   windows = ["test_wx.py"]
# line below.
#
#
# Run the build process by entering 'setup.py py2exe' or
# 'python setup.py py2exe' in a console prompt.
#
# If everything works well, you should find a subdirectory named 'dist'
# containing some files, among them hello.exe and test_wx.exe.


from distutils.core import setup
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.0.0.1"
        self.company_name = "No Company"
        self.copyright = "dreamfly copyright"
        self.name = "Http download"
	self.description = "Http download script"
		
manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24
target = Target(
    # used for the versioninfo resource
    description = "A sample app",

    # what to build
    script = "HttpDownload.py",
    #other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="HttpDownload"))],
##    icon_resources = [(1, "icon.ico")],
    dest_base = "HttpDownload")

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "1.0.0.1",
    company_name = "No Company",
    copyright = "dreamfly copyright",
    name = "Http download",
    description = "Http download script" ,   
    zipfile = "library.dll",
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "bundle_files": 1}},

    # targets to build
    console = ["HttpDownload.py"],
    )
