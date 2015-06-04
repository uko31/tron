#!/usr/bin/python

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Things to do and ideas:
#    - déterminer le vainqueur! (done!)
#    - permettre des lignes plus grosses (done!)
#    - habiller l'écran (boost indicator, player names, menu ('quit', 'settings', 'start', 'stop'))
#    - mettre en place un décompte d'avant départ.
#    - mettre en place la recharge du turbo recharge de 1 tous les X ticks (Fait!)
#    - faire apparaitre les garages de départ (Fait!)
#    - mettre en place un team play (plusieurs joueurs contre 1)
#    - mettre en place la notion de longeur de trace (avec fade progressif)
#    - capture the flag
#    - bonus ghost pour disparaitre sans laisser de trace pendant quelques ticks (? interet)
#    - Mettre un frein sur la touche <Down> (et assimilées)
#    - Changer la forme de la "tête" du Pod
#    - Gérer la gestion des bonus
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Libraries
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

from tkinter import *
from tkinter import ttk
import math
import time
import threading
import os.path
import json

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Program Configuration Variables
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

_SETTING_FILE_ = "./tron.json"

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Classes
#       Setting: setting file interface (load, save, update)
#       Game: Game settings and static Objects reference
#       MainWindow: do i need to explain ?
#       SettingWindow: Edit&Update Settings via interface
#       TronFrame: the frame that hosts the game
#       Pod: Control Pod, each pod is an instance, each instance run in a
#            separate thread.
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class Setting:
    def __init__(self, filename):
        self.filename = filename
        
        if not self.Read():
            sys.exit("Settings.__init__ CRITICAL Unable to read settings from file: [%s]" % self.filename)

    def Read(self):
        if os.path.isfile(self.filename):
            try:
                fd = open(self.filename, "r")
                setting = dict(json.load(fd))
                for key, val in setting["general"].items():
                    Game.Setting[key] = val
                    
                Game.InitStartPositions()
                
                for pod in setting["pods"]:
                    Game.Podlist.append(pod),
                    # Game.Pod[pod["id"]] = Pod( name       = pod["name"],
                                               # direction  = Game.StartPosition[pod["position"]]["direction"],
                                               # coord      = Game.StartPosition[pod["position"]],
                                               # left       = pod["left_key"], 
                                               # right      = pod["right_key"],
                                               # boost      = pod["boost_key"],
                                               # color      = pod["color"],
                                               # outline    = pod["outline"] )
                    
                fd.close()
                return(True)
            
            except IOError as e:
                print("Settings.Read ERROR tryin to open [%s]" % (e.info, self.filename))
                return(False)
        else:
            return(False)

class Game:
    Pod     = dict()
    Podlist = list()
    Setting = dict()
    Field   = None
    StartPosition = dict()
    
    @staticmethod
    def InitStartPositions():
        Game.StartPosition["West"]  = {'x': 20, 'y' : Game.Setting["height"] / 2, "direction": 0 }
        Game.StartPosition["East"]  = {'x': Game.Setting["width"] - 20 - Game.Setting["thickness"] - Game.Setting["interval"], 'y': Game.Setting["height"] / 2, "direction": 180 }
        Game.StartPosition["North"] = {'x': Game.Setting["width"] / 2, 'y': 20, "direction": 90 }
        Game.StartPosition["South"] = {'x': Game.Setting["width"] / 2, 'y': Game.Setting["height"] - 20  - Game.Setting["thickness"] - Game.Setting["interval"], "direction": 270 }
    
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.statusBarText = StringVar()
        self.statusBarText.set("Press F1-4 to start a game.")
        self.players = list()
        self.start_positions = dict()
        
        self.InitMenu()
        self.InitUI()
        self.DrawUI()
        self.InitPlayers()

    def InitMenu(self):
        self.menu = Menu(self.root)
        
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="1 Player Game",  command=lambda nb=1: self.tronFrame.Start(nb), accelerator="F1")
        self.fileMenu.add_command(label="2 Players Game", command=lambda nb=2: self.tronFrame.Start(nb), accelerator="F2")
        self.fileMenu.add_command(label="3 Players Game", command=lambda nb=3: self.tronFrame.Start(nb), accelerator="F3")
        self.fileMenu.add_command(label="4 Players Game", command=lambda nb=4: self.tronFrame.Start(nb), accelerator="F4")
        self.fileMenu.add_command(command=quit, label="**New Game... (CTRL+N)")     #allow to set a game setting and start
        self.fileMenu.add_command(command=quit, label="**Restart Game (CTRL+R)")    #must be grayed when no game has been set
        self.fileMenu.add_separator()   
        self.fileMenu.add_command(command=quit, label="Quit (CTRL+Q)")              #must be grayed when no game has been set
        
        self.settingMenu = Menu(self.menu, tearoff=0)
        self.settingMenu.add_command(command=quit, label="**Settings... (CTRL+S)")  #edit&save new settings

        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Settings", menu=self.settingMenu)
        
        self.root.config(menu = self.menu)
        self.root.bind("<F1>", lambda e, n = 1: self.tronFrame.NewGame(n, e))
        self.root.bind("<F2>", lambda e, n = 2: self.tronFrame.NewGame(n, e))
        self.root.bind("<F3>", lambda e, n = 3: self.tronFrame.NewGame(n, e))
        self.root.bind("<F4>", lambda e, n = 4: self.tronFrame.NewGame(n, e))
        
    def InitUI(self):
        self.topFrame    = Frame(self.root)
        self.mainFrame   = Frame(self.root)
        self.bottomFrame = Frame(self.root)
        
        self.tronFrame   = TronFrame(self.mainFrame, self.statusBarText, self.players) #, self.settings)
        
        self.statusBar   = Label(self.bottomFrame, textvariable = self.statusBarText, anchor=W)
    
    def DrawUI(self):
        Grid.rowconfigure   (self.root, 0, weight=1)                                 # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.root, 0, weight=1)                                 # set weight=1 to authorize resizing element
        Grid.rowconfigure   (self.mainFrame, 0, weight=1, minsize=Game.Setting["height"])  # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.mainFrame, 0, weight=1, minsize=Game.Setting["width"])   # set weight=1 to authorize resizing element    

        self.topFrame.grid  (row=0, column=0)
        self.mainFrame.grid  (row=1, column=0)
        self.bottomFrame.grid(row=2, column=0)
        
        self.statusBar.grid(row=0, column=0, sticky=W)
        
    def InitPlayers(self):
        for pod in Game.Pod:
            self.players.append(pod)

class SettingWindow:
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
        
        if not self.Read():
            sys.exit("Settings.__init__ CRITICAL Unable to read settings from file: [%s]" % self.filename)
            
        self.InitUI()
        self.DrawUI()
    
    def InitUI(self):
        self.setSpeedLabel      = Label(self.root, text = "Set Speed")
        self.setDelayLabel      = Label(self.root, text = "Set Delay")
        self.setThicknessLabel  = Label(self.root, text = "Set Thickness")
        self.setWidthLabel      = Label(self.root, text = "Set Widht")
        self.setHeightLabel     = Label(self.root, text = "Set Height")
        self.setResizeLabel     = Label(self.root, text = "Set Resize (on/off)")
        self.setBoostDelayLabel = Label(self.root, text = "Set Boost Delay")

        self.setSpeedEntry      = Entry(self.root, textvariable = self.speed)
        self.setDelayEntry      = Entry(self.root, textvariable = self.delay)
        self.setThicknessEntry  = Entry(self.root, textvariable = self.thickness)
        self.setWidthEntry      = Entry(self.root, textvariable = self.width)
        self.setHeightEntry     = Entry(self.root, textvariable = self.height)
        self.setResizeCheckbox  = Checkbutton(self.root, variable = self.resize )
        self.setBoostDelayEntry = Entry(self.root, textvariable = self.boost_delay)
        
        self.saveButton = Button(self.root, text="Save", command=self.Write)
        self.cancelButton = Button(self.root, text="Cancel", command=self.Cancel)
        self.reloadButton = Button(self.root, text="Reload", command=self.Read)
        
    def DrawUI(self):
        self.setSpeedLabel.grid     (row=0, column=0)
        self.setDelayLabel.grid     (row=1, column=0)
        self.setThicknessLabel.grid (row=2, column=0)
        self.setWidthLabel.grid     (row=3, column=0)
        self.setHeightLabel.grid    (row=4, column=0)
        self.setResizeLabel.grid    (row=5, column=0)
        self.setBoostDelayLabel.grid(row=6, column=0)
        
        self.setSpeedEntry.grid     (row=0, column=1)
        self.setDelayEntry.grid     (row=1, column=1)
        self.setThicknessEntry.grid (row=2, column=1)
        self.setWidthEntry.grid     (row=3, column=1)
        self.setHeightEntry.grid    (row=4, column=1)
        self.setResizeCheckbox.grid (row=5, column=1)
        self.setBoostDelayEntry.grid(row=6, column=1)
        
        self.reloadButton.grid(row=7, column=0)
        self.cancelButton.grid(row=7, column=1)
        self.saveButton.grid  (row=7, column=1)
        
    def Read(self):
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
        if not self.Read():
            sys.exit("Settings.__init__ CRITICAL Unable to read settings from file: [%s]" % self.filename)
            
class TronFrame:
    #HEIGHT, WIDTH = 800, 800
    
    def __init__(self, root, text, players):
        self.root = root
        self.text = text
        self.players = players
        
        self.InitUI()
        self.DrawUI()
        self.DrawGarages()
        # self.NewGame()

    def InitUI(self):
        self.canvas = Canvas(self.root)
        Game.Field  = self.canvas # for futur and outside class reference

        
    def DrawUI(self):
        Grid.rowconfigure   (self.canvas, 0, weight=1, minsize=Game.Setting["height"])  # set weight=1 to authorize resizing element in row[0] main.canvas
        Grid.columnconfigure(self.canvas, 0, weight=1, minsize=Game.Setting["width"])  # set weight=1 to authorize resizing element in column[0] main.canvas

        self.canvas.grid(row=0, column=0, sticky=E+S+W+N)
        self.canvas.focus_set()
        
    def NewGame(self, n, event=None):
        for pod in Game.Podlist:
            if pod["id"] in Game.Pod:
                print("il existe encore au moins un Pod")
                return(False)
    
        for pod in Game.Podlist:
            Game.Field.delete(pod["name"])
            
        for pod in Game.Podlist:
            if pod["id"] <= n:
                Game.Pod[pod["id"]] = Pod( name       = pod["name"],
                                           direction  = Game.StartPosition[pod["position"]]["direction"],
                                           coord      = Game.StartPosition[pod["position"]],
                                           left       = pod["left_key"], 
                                           right      = pod["right_key"],
                                           boost      = pod["boost_key"],
                                           color      = pod["color"],
                                           outline    = pod["outline"] )
                Game.Pod[pod["id"]].start()
    
    # def Start(self, n):
        # i = 1
        # for pod in Game.Pod:
            # Game.Pod[pod].start()
            # if i == n:
                # break
            # else:
                # i += 1
            
    def DrawGarages(self):
        for position in Game.StartPosition:
            garage = Pod( "garage",
                          direction = Game.StartPosition[position]["direction"],
                          coord     = Game.StartPosition[position],
                          left      = None,
                          right     = None,
                          boost     = None,
                          color     = "#808080",
                          outline   = "#1A1A1A" )
            garage.Turn(Pod.LEFT)
            garage.Move(ghost = True)
            garage.Turn(Pod.LEFT)
            garage.Move()
            garage.Turn(Pod.LEFT)
            garage.Move()
            garage.Move()
            garage.Turn(Pod.LEFT)
            garage.Move()
            garage.Turn(Pod.LEFT)
            garage.Move()

class Pod(threading.Thread):
    # class static attributes
    EAST, SOUTH, WEST, NORTH = 0, 90, 180, 270
    ANGLE = 90
    LEFT, RIGHT = -ANGLE, ANGLE
    TICKS = 10
    
    def __init__( self, 
                  name,
                  direction, 
                  coord,
                  left, right, boost,
                  color, outline):
        
        threading.Thread.__init__(self)
        
        self.name      = name
        self.direction = direction
        self.interval  = int(Game.Setting["interval"])
        self.thickness = int(Game.Setting["thickness"])
        self.x, self.y = coord['x'], coord['y'],
        self.left      = left,
        self.right     = right,
        self.boost     = boost,
        self.color     = color,
        self.outline   = outline,
        self.go        = True
        
        self.delay = Game.Setting["delay"]
        self.ticks = 0
    
    def run(self):
        Game.Field.bind(self.left,  lambda event, angle=Pod.LEFT : self.Turn(angle))
        Game.Field.bind(self.right, lambda event, angle=Pod.RIGHT: self.Turn(angle))
        Game.Field.bind(self.boost, self.Boost)
        
        while self.go:
            if self.ticks > 0:
                self.ticks -= 1
                if self.ticks == 0:
                    self.EndBoost()
            
            if self.Collision():
                self.go = False
            self.Move()
            time.sleep(self.delay)
        
        for pod in Game.Podlist:
            if pod["name"] == self.name:
                del(Game.Pod[pod["id"]])
    
    def Collision(self):
        xoff = self.x + int((self.interval + self.thickness) * math.cos(math.radians(self.direction)))
        yoff = self.y + int((self.interval + self.thickness) * math.sin(math.radians(self.direction)))

        # test if Pod is out of Frame:
        if xoff < 0  or xoff + self.thickness > Game.Setting["width"]  or yoff < 0 or yoff + self.thickness > Game.Setting["height"]:
            print("[%s] out of field, he is gameover" % self.name)
            return(True)
        
        # test if Pod crossed a track:
        elif Game.Field.find_overlapping(xoff, yoff, xoff + self.thickness, yoff + self.thickness):
            print("[%s] overlapped, he is gameover" % self.name)
            return(True)
        
        # else you're good to go:
        else:
            return(False)


    def Move(self, ghost=False):
        if ghost == False:
            Game.Field.create_rectangle( self.x, 
                                         self.y, 
                                         self.x + self.thickness, 
                                         self.y + self.thickness,
                                         tag = self.name,
                                         fill    = self.color,
                                         outline = self.outline )
        self.x += int((self.interval + self.thickness) * math.cos(math.radians(self.direction)))
        self.y += int((self.interval + self.thickness) * math.sin(math.radians(self.direction)))
        
    
    def Turn(self, angle, event=None):
        self.direction = (self.direction + angle) % 360
        
    def Boost(self, event=None):
        self.delay /= 4
        self.ticks =  Pod.TICKS
        
    def EndBoost(self, event=None):
        self.delay *= 4

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Main Program
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if __name__ == "__main__":
    
    setting = Setting(_SETTING_FILE_)
    
    TronApp = Tk()
    TronApp.title("Tron Clone")                                     # application title
    #TronApp.geometry("%dx%d" % (TronFrame.WIDTH, TronFrame.HEIGHT)) # set window size
    TronApp.resizable(width=False, height=False)                    # unable window resizing
    
    tron = MainWindow(TronApp)                                       # init main application Frame inside App

    TronApp.mainloop()
