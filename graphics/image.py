import win32ui
import win32gui
import win32con
import win32api
import graphics.bitmap as bitmap


class Image:
    def __init__(self, width, height, bitsperpixel, bits) -> None:
        self.width = width
        self.height = height
        self.bitsperpixel = bitsperpixel
        self.bits = bits

    def save(self, filename):
        size = (self.width, self.height)

        #add header of bitmap to bitmap bits
        data = bitmap.BITMAPHEADER(size, self.bitsperpixel) + self.bits

        #write data to file
        with open(filename, "wb") as file:
            file.write(data)


def frombuffer(bytes):
    #read information about bitmap
    header = bitmap.BITMAPINFO(bytes)

    #skip header and read rest of bits 
    bits = bytes[54::]

    return Image(width=header["width"], height=header["height"], bitsperpixel=header["Bits Per Pixel"], bits=bits)


def load(path):
    with open(path, "rb") as file:
        data = file.read()

    return frombuffer(data)

def screen_size(all_monitors=False):
    if all_monitors:
        a, b = 78, 79
    else:
        a, b = 0, 1

    #get width from system
    width = win32api.GetSystemMetrics(a)

    #get height from system
    height = win32api.GetSystemMetrics(b)
    return width, height


def screenshot(windowname:str=None, crop:tuple[int, int, int, int] = None):
    if crop == None and windowname == None:
        width, height = screen_size()
        x,y = 0,0

    elif windowname != None:
        hwnd = win32gui.FindWindow(None, windowname)
        placement = win32gui.GetWindowPlacement(hwnd)

        if placement[1] == win32con.SW_SHOWMAXIMIZED:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
            
        x, y, width, height = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, width-x, height-y, 0)

    elif crop != None:
        x, y, width, height = crop
        width += x
        height += y


    wDC = win32gui.GetWindowDC(0)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width-x, height-y)
    cDC.SelectObject(dataBitMap)

    #paint bitmap
    cDC.BitBlt((0,0),(width-x, height-y) , dcObj, (x,y), win32con.SRCCOPY)

    #read bits from bitmap object
    bits = dataBitMap.GetBitmapBits(True)

    #get information about bitmap
    info = dataBitMap.GetInfo()

    #free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(0, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return Image(width=info["bmWidth"], height=info["bmHeight"], bitsperpixel=info["bmBitsPixel"], bits=bits)



  
