import winapi
import graphics as gpu
import time
import json
import os


def get_settings(path:str = None):
    if path == None:
        path = "settings.json" 

    #check if settings file exists
    if os.path.isfile(path) == True:

        #read settings from json file
        with open(path, "r") as Jsonfile:
            settings = json.loads(Jsonfile.read())

    else:
        data = {"auto exit": True,"echo": True, "delay": 0}

        with open(path, "w") as JsonFile:
            json.dump(data, JsonFile, indent=4)

        return get_settings(path)
            

    return settings



class AutoAccept:
    def __init__(self, settings) -> None:
        self.process_name = "csgo.exe"
        self.title = "Counter-Strike: Global Offensive"
        self.rect = None
        self.size = 1920, 1080
        self.display = 0
        self.bit = b'P\xafL\xff'
        self.box_width = 128
        self.box_height = 5
        self.settings = settings


    def run(self):
        #set echo variable
        echo = self.settings["echo"]
        delay = self.settings["delay"]

        if echo: print(time.strftime("[%H:%M:%S] - Started program"))

        #wait until process csgo.exe is alive
        while not winapi.is_process_alive(self.process_name): 
            time.sleep(1)

        if echo: print(time.strftime("[%H:%M:%S] - Counter-Strike: Global Offensive is on"))

        #read information about csgo window
        self.GameInfo()
        
        similar = False
        while not similar:
            #calculate screenshot box
            box = self.button_box()

            #take screenshot
            img = gpu.screenshot(crop=box)
            
            #check if image is the same as original accept button
            similar = self.check_image(img.bits)

        
        #calculate position for mouse
        pos = (self.size[0]//2 + self.size[0]*self.display, self.top_distance()+10)

        #move mouse
        winapi.mouse_move(pos)
        
        #add delay
        if delay > 0 and delay <= 20: time.sleep(delay)

        #click left button
        winapi.click(pos)

        if echo: print(time.strftime("[%H:%M:%S] - Matchmaking has been accepted"))

        if self.settings["auto exit"] == True:
            exit(0)
        else:
            input("Press any button to exit...")


    def check_image(self, bits):
        #draw original image, every pixel of this image have the same color
        original = self.bit*self.box_width*self.box_height
        return original==bits
        

    def top_distance(self):
        height = self.size[1]
        return int((11/30) * height +9) + 5
    

    def button_box(self):
        #crop contain 4 values which are: startX, startY, width, height
        crop = (self.size[0]//2 - self.box_width//2 + self.size[0]*self.display, 
                self.top_distance(), 
                self.box_width, 
                self.box_height)

        return crop


    def GameInfo(self):
        #get full title of window
        self.title = [s for s in winapi.listWindows() if self.title in s][0]

        #get rect of  window
        self.rect = winapi.rect(self.title)

        #write size of window
        self.size = self.rect[2]-self.rect[0],  self.rect[3]-self.rect[1]

        #check which display the window is on
        self.display = self.rect[0]//self.rect[3]




