#!/usr/bin/python

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Author : m.gregoriades@gmail.com
#   Date   : 2015-05-25
#   Version: 0.1
#   History: 
#        None
#
#   Things to do/ideas:
#    - déterminer le vainqueur! (done!)
#    - permettre des lignes plus grosses (done!)
#    - habiller l'écran (boost indicator, player names, 
#      menu ('quit', 'settings', 'start', 'stop'))
#    - mettre en place la recharge du turbo recharge de 1 tous les X ticks
#    - faire apparaitre les garages de départ
#    - mettre en place un team play (plusieurs joueurs contre 1)
#    - mettre en place la notion de longeur de trace (avec fade progressif)
#    - capture the flag
#    - bonus ghost pour disparaitre sans laisser de trace pendant quelques 
#      ticks (? interet)
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Standard Libraries:
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

from   tkinter import *
import time
import threading
import json
import os.path

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Settings:
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

_SPEED_       = 1
_HEIGHT_      = 500
_WIDTH_       = 500
_RESIZE_      = False
_THICK_       = 6
_DELAY_       = 0.02
_BOOST_DELAY_ = 25
_Settings_Filename_ = "./tron.json"

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Classes:
#       MainWindow => main window...
#       TronFrame  => the frame that host the game
#       Settings   => handle settings changes, saves & loads
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

Class MainWindow:
    def __init__(self, root, width, height, resize):
        self.root   = root
        self.width  = width
        self.height = height
        self.resize = resize                                                    #boolean expected
        
        self.settings = Settings(self.root, _Settings_Filename_)                #Settings are loaded from the Settings class
        
        self.initMenu()
        self.initUI()
        self.drawUI()

    def initMenu(self):
        self.menu = Menu(self.root)
        
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(command=quit, label="**New Game... (CTRL+N)")   #allow to set a game setting and start
        self.fileMenu.add_command(command=quit, label="**Restart Game (CTRL+R)")  #must be grayed when no game has been set
        self.fileMenu.add_separator()
        self.fileMenu.add_command(command=quit, label="Quit (CTRL+Q)")          #must be grayed when no game has been set
        
        self.settingMenu = Menu(self.menu, tearoff=0)
        self.settingMenu.add_command(command=quit, label="**Settings... (CTRL+S)")#edit&save new settings

        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Settings", menu=self.settingsMenu)
        
    def initUI(self):
        self.topFrame    = Frame(self.root)
        self.mainFrame   = Frame(self.root)
        self.bottomFrame = Frame(self.root)
        
        self.tronFrame   = TronFrame(self.mainFrame, self.settings)
    
    def drawUI(self):
        Grid.rowconfigure   (self.root, 0, weight=1)                            # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.root, 0, weight=1)                            # set weight=1 to authorize resizing element
        Grid.rowconfigure   (self.mainFrame, 0, weight=1, minsize=self.height)  # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.mainFrame, 0, weight=1, minsize=self.width)   # set weight=1 to authorize resizing element    

        self.tropFrame.grid  (row=0, column=0)
        self.mainFrame.grid  (row=0, column=0)
        self.bottomFrame.grid(row=0, column=0)

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
                
                self.speed.set      (settings["speed"])
                self.delay.set      (settings["delay"])
                self.thickness.set  (settings["thickness"])
                self.width.set      (settings["width"])
                self.height.set     (settings["height"])
                self.resize.set     (settings["resize"])
                self.boost_delay.set(settings["boost_delay"])
                
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
    def __init__(self, root, settings):
        self.root = root
        self.settings = settings
        
        self.speed = speed
        self.players = list()
        
        self.InitMenu()
        self.InitUI()
        self.DrawUI()
        self.InitStartPositions()
    
    def InitMenu(self):
        self.menuBar  = Menu(self.root)
        self.gameMenu = Menu(self.menuBar, tearoff=0)
        self.gameMenu.add_command(label="New Game", command=self.newGame)
        self.gameMenu.add_command(label="Settings...", command=self.settings)
        self.gameMenu.add_separator()
        self.gameMenu.add_command(label="Quit", command=quit)
        self.menuBar.add_cascade(label="Game", menu=self.gameMenu)
        
        self.root.config(menu = self.menuBar)
        
    def newGame(self):
        print("NewGame... to be done.")
    
    def settings(self):
        print("Settings... to be done.")

    def InitUI(self):
        self.canvas = Canvas(self.root, bd=2)
        self.canvas.bind('<Key>', self.Start)
        
    def DrawUI(self):
        Grid.rowconfigure   (self.root, 0, weight=1)                 # set weight=1 to authorize resizing element in row[0] main.root
        Grid.columnconfigure(self.root, 0, weight=1)                 # set weight=1 to authorize resizing element in column[0] main.root
        
        Grid.rowconfigure   (self.canvas, 0, weight=1, minsize=500)  # set weight=1 to authorize resizing element in row[0] main.canvas
        Grid.columnconfigure(self.canvas, 0, weight=1, minsize=500)  # set weight=1 to authorize resizing element in column[0] main.canvas

        self.canvas.grid(row=0, column=0, sticky=E+S+W+N)
        self.canvas.focus_set()

    def InitStartPositions(self):
        self.start_positions = dict()
        self.start_positions['West']  = {'x' : 20,           'y' : _HEIGHT_ / 2  }
        self.start_positions['East']  = {'x' : _WIDTH_ - 20, 'y' : _HEIGHT_ / 2  }
        self.start_positions['North'] = {'x' : _WIDTH_ / 2,  'y' : 20            }
        self.start_positions['South'] = {'x' : _WIDTH_ / 2,  'y' : _HEIGHT_ - 20 }

        self.drawGarage(self.start_positions['West'], 'East')
        self.drawGarage(self.start_positions['East'], 'West')
        self.drawGarage(self.start_positions['North'], 'South')
        self.drawGarage(self.start_positions['South'], 'North')
