import win32gui
import pyautogui
import time

def enum_window_titles():
    def callback(handle, data):
        titles.append(win32gui.GetWindowText(handle))
    titles = []
    win32gui.EnumWindows(callback, None)
    return titles

mydir = 'D:\\YouTube\\REAL LIFE JARVIS\\Notes'
entered = False
import face_login
while True:
    
    working = enum_window_titles()
    #print(mydir not in working , entered==True)
    if mydir not in working and entered==True:
        entered = False
        
    elif (mydir in working and entered==True) or (mydir not in working and entered==False):
        pass
    
    else:
        log,r = face_login.face_recognition_realtime()
        if log==False:
            pyautogui.hotkey('alt', 'f4')
            entered = False
        else:
            
            entered = True
            
        r.destroy()
        



    
