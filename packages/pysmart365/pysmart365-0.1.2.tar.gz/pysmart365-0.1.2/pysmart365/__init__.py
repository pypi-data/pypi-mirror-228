AUTHOR = 'Runkang'
COPYRIGHT = '© Copyright 2023 Informatic365 - SmartSoft - MicroSoftware'
import subprocess
import platform
from customtkinter import *
from tkinter import messagebox
import sys
import time
import threading as th

def turn_off(time: float=0) -> None:
    '''
    Shutdown pc directly without gui graphics.
    '''
    subprocess.run(['shutdown', '-s', '-t', f'{time}'])
def restart(time: float=0) -> None:
    '''
    Restart pc with or without time
    '''
    subprocess.run(['shutdown', '-r', '-t', f'{time}'])
def restart_with_advancedmode(time: float=0) -> None:
    '''
    Restart pc to advanced mode available on Windows 10 and 11 or successive version.
    '''
    subprocess.run(['shutdown', '-r', '-o', '-t', f'{time}'])
def turn_off_with_gui():
    '''
    Turn Off pc with gui available on Windows 10 and 11 or successive version.
    '''
    check_windows_version = platform.win32_ver()[0]
    if check_windows_version == '7' or '8':
        pass
    else:
        subprocess.run(['slidetoshutdown'])
def set_copyright(year: str, company: str) -> None:
    '''
    Enter the copyright text that will be displayed with the name that you can customize and the year using the attribute 'company' for the name and 'year' for the year.
    Example if i write copyright_view(year='2022 - 2023', company= 'Informatic365')
    then displays "© Copyright 2022 - 2023 Informatic365".
    '''
    get = f'© Copyright {year} {company}'
    return get
class close():
    def __init__(self, delay: float=0) -> None:
        def set():
            time.sleep(delay)
            sys.exit()
        th.Thread(target=set).start()

class wincenter():
    def __init__(self, width, height) -> None:
        swidth = CTk().winfo_screenwidth()
        sheight = CTk().winfo_screenheight()
        x = (swidth - width) // 2
        y = (sheight - height) // 2
        
        self.set = f"{width}x{height}+{x}+{y}"

class msbox():
    def showinfo(self, title, message) -> None:
        messagebox.showinfo(title=title, message=message)
    def showerror(self, title, message) -> None:
        messagebox.showerror(title=title, message=message)
    def show_warning(self, title, message):
        messagebox.showwarning(title=title, message=message)