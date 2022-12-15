import struct

def BITMAPHEADER(resolution:tuple, BitsPerPixel:int):
    #function creates bitmap header

    offset = 54
    width, height = resolution
    RawSize = width*height *int(BitsPerPixel/8)
    Size = RawSize + offset
    DIB_Header_Size = 40

    header = struct.pack("<2sIHHIIIIHHIIIIII",b'BM', Size, 0, 0, offset, DIB_Header_Size, width, height, 1, BitsPerPixel, 0, RawSize, 0, 0, 0, 0)

    return header


def BITMAPINFO(bmp:bytes):
    #function reads information from bitmap header
    header = bmp[:54]
    values = {}
    
    values["type"] = header[:2].decode()
    values["size"] = struct.unpack('I', header[2:6])[0]
    values["reserved 1"] = struct.unpack('H', header[6:8])[0]
    values["reserved 2"] = struct.unpack('H', header[8:10])[0]
    values["offset"] = struct.unpack('I', header[10:14])[0]
    values["DIB Header Size"] = struct.unpack('I', header[14:18])[0]
    values["width"] = struct.unpack('I',header[18:22])[0]
    values["height"] = struct.unpack('I', header[22:26])[0]
    values["Color Planes"] = struct.unpack('H', header[26:28])[0]
    values["Bits Per Pixel"] = struct.unpack('H', header[28:30])[0]
    values["Compression Method"] = struct.unpack('I', header[30:34])[0]
    values["Raw Image Size"] = struct.unpack('I', header[34:38])[0]
    values["Horizontal Resolution"] = struct.unpack('I', header[38:42])[0]
    values["Vertical Resolution"] = struct.unpack('I', header[42:46])[0]
    values["Number of Colors"] = struct.unpack('I', header[46:50])[0]
    values["Important Colors"] = struct.unpack('I', header[50:54])[0]
    return values