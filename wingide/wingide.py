#!/usr/bin/python3
#-*-encoding:utf8-*-

import os
import string
import random
import hashlib
import platform
# GUI Import
py_version = platform.python_version()
is_py3 = py_version[0] == '3' and True or False
if is_py3 == True:
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
else:
    from Tkinter import *
    import ttk
    import tkMessageBox as messagebox    


BASE16 = '0123456789ABCDEF'
BASE30 = '123456789ABCDEFGHJKLMNPQRTVWXY'

g_version_list = ('8.X.X', '7.X.X', '6.X.X', '5.X.X')
g_version_magics = {
    '5.X.X': [7, 123, 23, 87],
    '6.X.X': [23, 161, 47, 9],
    '7.X.X': [221, 13, 93, 27],
    '8.X.X': [179, 95, 45, 245],
}

def RandomString(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join((random.choice(chars) for _ in range(size)))


def BaseConvert(number, fromdigits, todigits, ignore_negative=True):
    if not ignore_negative and str(number)[0] == '-':
        number = str(number)[1:]
        neg = 1
    else:
        neg = 0
        
    x = 0
    for digit in str(number):
        x = x * len(fromdigits) + fromdigits.index(digit)

    res = ''
    while x > 0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x //= len(todigits)

    if neg:
        res = '-' + res
        
    return res


def AddHyphens(code):
    return code[:5] + '-' + code[5:10] + '-' + code[10:15] + '-' + code[15:]


def SHAToBase30(digest):
    tdigest = ''.join([c for i, c in enumerate(digest) if i // 2 * 2 == i])
    result = BaseConvert(tdigest, BASE16, BASE30)
    while len(result) < 17:
        result = '1' + result
        
    return result


def loop(ecx, lichash):
    part = 0
    for c in lichash:
        part = ecx * part + ord(c) & 1048575
        
    return part


def CalcActivationCode(args):
    if not isinstance(args, Application):
        return
    
    # # Generate License ID
    # licenseID = AddHyphens('CN' + RandomString(18, '123456789ABCDEFGHJKLMNPQRTVWXY'))
    licenseID = args.LicID.get()
    print ('License id: ' + licenseID)
    
    #requestCode = input('Enter request code:')
    requestCode = args.ReqCode.get()
    print ('Request code: ' + requestCode)
    if requestCode.strip() == '':
        messagebox.showerror("Hints", "Please input the Request Code !")
        return 
    
    # # SHA1
    shaHasher = hashlib.sha1()
    shaHasher.update(requestCode.encode('utf-8'))
    shaHasher.update(licenseID.encode('utf-8'))
    hashResult = shaHasher.hexdigest().upper()
    lichash = AddHyphens(requestCode[:3] + SHAToBase30(hashResult))

    versionMagic = None
    # Supported crack WingIDE Pro version list : 5.x.x, 6.x.x, 7.x.x, 8.x.x
    wingIDEProVerStr = args.VersionInfo.get()
    print ('Cracking WingIDE Version : ' + wingIDEProVerStr)
    if wingIDEProVerStr in g_version_magics.keys():
        versionMagic = g_version_magics[wingIDEProVerStr]
    if versionMagic:
        activationCode = format(loop(versionMagic[0], lichash), '05x') + \
            format(loop(versionMagic[1], lichash), '05x') + \
            format(loop(versionMagic[2], lichash), '05x') + \
            format(loop(versionMagic[3], lichash), '05x')
    else:
        print('Get wrong WingIDE version, exit...')
        os._exit(0)
        
    activationCode = BaseConvert(activationCode.upper(), BASE16, BASE30)
    while len(activationCode) < 17:
        activationCode = '1' + activationCode

    activationCode = AddHyphens('AXX' + activationCode)
    print ('Activation code: ' + activationCode)
    args.ActCode.set(activationCode)
    pass


class Application(Frame):
    def __init__(self, master=None):
        if is_py3 == True: super().__init__(master) 
        else: Frame.__init__(self, master)
        
        scn_w, scn_h = master.winfo_screenwidth(), master.winfo_screenheight()
        win_w, win_h = 350, 180
        cen_x = (scn_w - win_w) / 2
        cen_y = (scn_h - win_h) / 2
        
        self.master = master
        self.master.title('WingIDE Pro Genkey (5, 6, 7, 8)')
        self.master.resizable(False, False) 
        self.master.geometry('%dx%d+%d+%d'%(win_w, win_h, cen_x, cen_y))
        self.create_widgets()
        pass

    def create_widgets(self):
        current_row = 0
        current_col = 0

        # Version Info
        self.l0 = Label(self.master, text='WingIDE Pro :')
        self.l0.grid(padx=5, pady=5, row=current_row, column=current_col, sticky=E)
        self.VersionInfo = StringVar()
        self.versionComb = ttk.Combobox(self.master, textvariable=self.VersionInfo, state='readonly')
        self.versionComb['values'] = g_version_list
        self.versionComb.grid(padx=5, pady=1, row=current_row, column=current_col + 1, sticky=W)
        self.versionComb.current(0)
        current_row += 1

        # License ID info
        self.l1 = Label(self.master, text='LicenseID:')
        self.l1.grid(padx=5, pady=5, row=current_row, column=current_col, sticky=E)
        self.LicID = StringVar()
        self.LicEntry = Entry(self.master, textvariable=self.LicID, width=30, state='readonly')
        self.LicEntry.grid(padx=5, pady=5, row=current_row, column=current_col + 1)
        self.LicID.set(AddHyphens('CN' + RandomString(18, '123456789ABCDEFGHJKLMNPQRTVWXY')))
        current_row += 1

        # Request code info
        self.l2 = Label(self.master, text='RequestCode:')
        self.l2.grid(padx=5, pady=5, row=current_row, column=current_col, sticky=E)
        self.ReqCode = StringVar()
        self.ReqcodeEntry = Entry(self.master, textvariable=self.ReqCode, width=30)
        self.ReqcodeEntry.grid(padx=5, pady=5, row=current_row, column=current_col + 1)
        current_row += 1

        # Activation code info
        self.l3 = Label(self.master, text=b'ActivationCode:')
        self.l3.grid(padx=5, pady=5, row=current_row, column=current_col, sticky=E)
        self.ActCode = StringVar()
        self.ReqcodeEntry = Entry(self.master, textvariable=self.ActCode, width=30, state='readonly')
        self.ReqcodeEntry.grid(padx=5, pady=5, row=current_row, column=current_col + 1)
        current_row += 1

        self.btn_Calc = Button(self.master)
        self.btn_Calc['text'] = 'Generate'
        self.btn_Calc['command'] = lambda: CalcActivationCode(self)
        self.btn_Calc.grid(padx=5, pady=5, row=current_row, columnspan=2, sticky=N + S)
        pass


if __name__ == '__main__':
    app = Application(master=Tk())
    app.mainloop()