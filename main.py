import winapi
import graphics as gpu
import time
import json


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


        #wait until process csgo.exe is alive
        while not winapi.is_process_alive(self.process_name): 
            time.sleep(1)

        print(time.strftime("[%H:%M:%S] - Counter-Strike: Global Offensive is on"))
        
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

            #delay to reduce memory usage
            time.sleep(0.05)

        
        if similar == True:
            #calculate position for mouse
            pos = (self.size[0]//2 + self.size[0]*self.display, self.top_distance()+10)

            #move mouse
            winapi.mouse_move(pos)

            #clicl left button
            winapi.click(pos)

        print(time.strftime("[%H:%M:%S] - Matchmaking has been accepted"))

        if settings["auto exit"] == True:
            exit(0)
        

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


if __name__ == "__main__":
    #read settings from json file
    with open("settings.json", "r") as Jsonfile:
        settings = json.loads(Jsonfile.read())

    
    print(time.strftime("[%H:%M:%S] - Started program"))

    AutoAccept(settings)

    input("Press any button to exit...")
