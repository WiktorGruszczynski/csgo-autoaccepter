import win32gui


def listWindows(hwnd = False):
    #create window list
    window_list = []

    def callback(hwnd, window_list):
        #add the title and handle of the window to the list
        window_list.append((win32gui.GetWindowText(hwnd), hwnd))

    #enumerate every active window
    win32gui.EnumWindows(callback, window_list)

    #check if hnwd is true ,if yes also assign hwnd value of window 
    if hwnd:
        window_list = [w for w in window_list if w[0] != '']
    else:
        window_list = [w[0] for w in window_list if w[0] != '']


    return window_list
    

def rect(windowname:str): 
    #get handle of window by name
    handle = win32gui.FindWindow(None, windowname)

    #get rect of window handle
    rect   = win32gui.GetWindowRect(handle)

    return rect
    

#1920x1080 (-8, -8, 1928, 1048)
