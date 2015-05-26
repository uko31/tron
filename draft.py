from tkinter import *
from tkinter import ttk
import json
import os.path

class Settings:
    def __init__(self, root, filename):
        self.root     = root
        self.filename = filename
        
        self.speed       = StringVar()
        self.delay       = StringVar()
        self.thickness   = StringVar()
        self.width       = IntVar()
        self.height      = IntVar()
        self.resize      = IntVar()
        self.boost_delay = IntVar()
        self.players     = list()
        
        if not self.Read():
            sys.exit("Settings.__init__ CRITICAL Unable to read settings from file: [%s]" % self.filename)
        
        self.InitUI()
        self.DrawUI()
    
    def InitUI(self):
        self.playerFrame = dict()
    
        self.nameLabel = dict()
        self.colorLabel = dict()
        self.positionLabel = dict()
        self.leftKeyLabel = dict()
        self.rightKeyLabel = dict()
        self.boostKeyLabel = dict()
        
        self.nameEntry = dict()
        self.colorEntry = dict()
        self.positionEntry = dict()
        self.leftKeyEntry = dict()
        self.rightKeyEntry = dict()
        self.boostKeyEntry = dict()
    
        self.generalSettings = ttk.LabelFrame(self.root, text="General Settings")
        self.playerSettings  = ttk.LabelFrame(self.root, text="Player Settings")
    
        self.setSpeedLabel      = Label(self.generalSettings, text = "Set Speed", width=22, anchor=W)
        self.setDelayLabel      = Label(self.generalSettings, text = "Set Delay", width=22, anchor=W)
        self.setThicknessLabel  = Label(self.generalSettings, text = "Set Thickness", width=22, anchor=W)
        self.setWidthLabel      = Label(self.generalSettings, text = "Set Widht", width=22, anchor=W)
        self.setHeightLabel     = Label(self.generalSettings, text = "Set Height", width=22, anchor=W)
        self.setResizeLabel     = Label(self.generalSettings, text = "Set Resize (on/off)", width=22, anchor=W)
        self.setBoostDelayLabel = Label(self.generalSettings, text = "Set Boost Delay", width=22, anchor=W)

        self.setSpeedEntry      = Entry(self.generalSettings, textvariable = self.speed)
        self.setDelayEntry      = Entry(self.generalSettings, textvariable = self.delay)
        self.setThicknessEntry  = Entry(self.generalSettings, textvariable = self.thickness)
        self.setWidthEntry      = Entry(self.generalSettings, textvariable = self.width)
        self.setHeightEntry     = Entry(self.generalSettings, textvariable = self.height)
        self.setResizeCheckbox  = Checkbutton(self.generalSettings, variable = self.resize)
        self.setBoostDelayEntry = Entry(self.generalSettings, textvariable = self.boost_delay)
        
        for player in self.playerName.keys():
            self.playerFrame[player] = LabelFrame(self.playerSettings, text=player)
        
            self.nameLabel[player]      = Label(self.playerFrame[player], text="Name", width=22, anchor=W)
            self.colorLabel[player]     = Label(self.playerFrame[player], text="Color", width=22, anchor=W)
            self.positionLabel[player]  = Label(self.playerFrame[player], text="Position", width=22, anchor=W)
            self.leftKeyLabel[player]   = Label(self.playerFrame[player], text="Left Key", width=22, anchor=W)
            self.rightKeyLabel[player]  = Label(self.playerFrame[player], text="Right Key", width=22, anchor=W)
            self.boostKeyLabel[player]  = Label(self.playerFrame[player], text="Boost Key", width=22, anchor=W)
            
            self.nameEntry[player]     = Entry(self.playerFrame[player], textvariable=self.playerName[player])
            self.colorEntry[player]    = Entry(self.playerFrame[player], textvariable=self.playerColor[player])
            self.positionEntry[player] = Entry(self.playerFrame[player], textvariable=self.playerPosition[player])
            self.leftKeyEntry[player]  = Entry(self.playerFrame[player], textvariable=self.playerLeftKey[player])
            self.rightKeyEntry[player] = Entry(self.playerFrame[player], textvariable=self.playerRightKey[player])
            self.boostKeyEntry[player] = Entry(self.playerFrame[player], textvariable=self.playerBoostKey[player])
            
        
        self.saveButton = Button(self.root, text="Save", command=self.Write)
        self.cancelButton = Button(self.root, text="Cancel", command=self.Cancel)
        self.reloadButton = Button(self.root, text="Reload", command=self.Read)
        
    def DrawUI(self):
        self.generalSettings.grid(row=0, column=0)
        self.playerSettings.grid (row=1, column=0)
   
        self.setSpeedLabel.grid     (row=0, column=0, sticky=W)
        self.setDelayLabel.grid     (row=1, column=0, sticky=W)
        self.setThicknessLabel.grid (row=2, column=0, sticky=W)
        self.setWidthLabel.grid     (row=3, column=0, sticky=W)
        self.setHeightLabel.grid    (row=4, column=0, sticky=W)
        self.setResizeLabel.grid    (row=5, column=0, sticky=W)
        self.setBoostDelayLabel.grid(row=6, column=0, sticky=W)
        
        self.setSpeedEntry.grid     (row=0, column=1)
        self.setDelayEntry.grid     (row=1, column=1)
        self.setThicknessEntry.grid (row=2, column=1)
        self.setWidthEntry.grid     (row=3, column=1)
        self.setHeightEntry.grid    (row=4, column=1)
        self.setResizeCheckbox.grid (row=5, column=1, sticky=W)
        self.setBoostDelayEntry.grid(row=6, column=1)

        i=0
        for player in self.playerName.keys():
            self.playerFrame[player].grid   (row=0+i, column=0)
        
            self.nameLabel[player] .grid    (row=0, column=0, sticky=W)
            self.colorLabel[player] .grid   (row=1, column=0, sticky=W)
            self.positionLabel[player] .grid(row=2, column=0, sticky=W)
            self.leftKeyLabel[player] .grid (row=3, column=0, sticky=W)
            self.rightKeyLabel[player] .grid(row=4, column=0, sticky=W)
            self.boostKeyLabel[player] .grid(row=5, column=0, sticky=W)

            self.nameEntry[player] .grid    (row=0, column=1)
            self.colorEntry[player] .grid   (row=1, column=1)
            self.positionEntry[player] .grid(row=2, column=1)
            self.leftKeyEntry[player] .grid (row=3, column=1)
            self.rightKeyEntry[player] .grid(row=4, column=1)
            self.boostKeyEntry[player] .grid(row=5, column=1)
            i+=1
        
        self.reloadButton.grid(row=7, column=0)
        # self.cancelButton.grid(row=7, column=1)
        self.saveButton.grid  (row=7, column=1)
        
    def Read(self):
        self.playerName = dict()
        self.playerColor = dict()
        self.playerPosition = dict()
        self.playerLeftKey = dict()
        self.playerRightKey = dict()
        self.playerBoostKey = dict()
    
        if os.path.isfile(self.filename):
            try:
                settings_file = open(self.filename, "r")
                settings = dict(json.load(settings_file))
                
                self.speed.set      (settings["general"]["speed"])
                self.delay.set      (settings["general"]["delay"])
                self.thickness.set  (settings["general"]["thickness"])
                self.width.set      (settings["general"]["width"])
                self.height.set     (settings["general"]["height"])
                self.resize.set     (settings["general"]["resize"])
                self.boost_delay.set(settings["general"]["boost_delay"])
                
                for player in settings["players"]:
                    self.playerName[player["name"]]     = StringVar()
                    self.playerColor[player["name"]]    = StringVar()
                    self.playerPosition[player["name"]] = StringVar()
                    self.playerLeftKey[player["name"]]  = StringVar()
                    self.playerRightKey[player["name"]] = StringVar()
                    self.playerBoostKey[player["name"]] = StringVar()
                
                    self.playerName[player["name"]].set(player["name"])
                    self.playerColor[player["name"]].set(player["color"])
                    self.playerPosition[player["name"]].set(player["position"])
                    self.playerLeftKey[player["name"]].set(player["left_key"])
                    self.playerRightKey[player["name"]].set(player["right_key"])
                    self.playerBoostKey[player["name"]].set(player["boost_key"])
                
                settings_file.close()
                return(True)
            except IOError as e:
                print("Settings.Read ERROR tryin to open [%s]" % (e.info, self.filename))
                return(False)
        else:
            return(False)
        
    def Write(self):
        if not os.path.isdir(os.path.dirname(self.filename)):
            print("Settings.Write WARNING configuration directory [%s] doesn't exists, trying to create it" % os.path.dirname(self.filename))
            try:
                os.makedirs(os.path.dirname(self.filename))
            except IOError as e:
                print("Settings.Write CRITICAL unable to create configuration file directory, reason [%s] => Exiting!" % e.info)
        try:
            settings_file = open(self.filename, "w")
            string = json.dump({"speed": "%s" % self.speed.get(),
                                "delay": "%s" % self.delay.get(),
                                "thickness": "%s" % self.thickness.get(),
                                "width": "%s" % self.width.get(), 
                                "height": "%s" % self.height.get(),
                                "resize": "%s" % self.resize.get(),
                                "boost_delay": "%s" % self.boost_delay.get()},
                               settings_file, indent = 4, sort_keys = True)
            settings_file.close()
        except IOError as e:
            print("Settings.Write ERROR while tryin to open [%s]" % (e.info, self.filename))
        
    def Cancel(Self):
        print("Settings.Cancel: to be coded...")
        
        
if __name__ == "__main__":
    testApp = Tk()
    
    s = Settings(testApp, ".\\test.json")
    
    testApp.mainloop()
    
    # if os.path.isfile(".\\test.json"):
        # settings_file = open(".\\test.json", "r")
        # settings = dict(json.load(settings_file))
        
        # print("General Settings: %s" % settings["General"])
        
        # for p in settings["Players"]:
            # print("%s Settings: %s" % (p["name"], p))

        # settings_file.close()
            
