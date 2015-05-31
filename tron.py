#!/usr/bin/python

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Things to do and ideas:
#    - déterminer le vainqueur! (done!)
#    - permettre des lignes plus grosses (done!)
#    - habiller l'écran (boost indicator, player names, menu ('quit', 'settings', 'start', 'stop'))
#
#    - mettre en place la recharge du turbo recharge de 1 tous les X ticks (Fait!)
#    - faire apparaitre les garages de départ (Fait!)
#    - mettre en place un team play (plusieurs joueurs contre 1)
#    - mettre en place la notion de longeur de trace (avec fade progressif)
#    - capture the flag
#    - bonus ghost pour disparaitre sans laisser de trace pendant quelques ticks (? interet)
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

from tkinter import *
from tkinter import ttk
import math
import time
import threading

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Program Configuration Variables
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

# None: they have been moved into classes static variables.

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Classes
#       TronFrame: the frame that hosts the gameove
#       Pod: each instance is 
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class MainWindow:
    def __init__(self, root):
        self.root = root
        
        #self.settings = Settings(self.root, _Settings_Filename_)                #Settings are loaded from the Settings class
        
        self.InitMenu()
        self.InitUI()
        self.DrawUI()

    def InitMenu(self):
        self.menu = Menu(self.root)
        
        self.fileMenu = Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="1 Player Game (F1)",  command=lambda nb=1: self.tronFrame.Start(nb), accelerator="<F1>")
        self.fileMenu.add_command(label="2 Players Game (F2)", command=lambda nb=2: self.tronFrame.Start(nb), accelerator="<F2>")
        self.fileMenu.add_command(label="3 Players Game (F3)", command=lambda nb=3: self.tronFrame.Start(nb), accelerator="<F3>")
        self.fileMenu.add_command(label="4 Players Game (F4)", command=lambda nb=4: self.tronFrame.Start(nb), accelerator="<F4>")
        self.fileMenu.add_command(command=quit, label="**New Game... (CTRL+N)")     #allow to set a game setting and start
        self.fileMenu.add_command(command=quit, label="**Restart Game (CTRL+R)")    #must be grayed when no game has been set
        self.fileMenu.add_separator()   
        self.fileMenu.add_command(command=quit, label="Quit (CTRL+Q)")              #must be grayed when no game has been set
        
        self.settingMenu = Menu(self.menu, tearoff=0)
        self.settingMenu.add_command(command=quit, label="**Settings... (CTRL+S)")  #edit&save new settings

        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="Settings", menu=self.settingMenu)
        
        self.root.config(menu = self.menu)
        self.root.bind("<F1>", lambda nb=1: self.tronFrame.Start(nb))
        
    def InitUI(self):
        self.topFrame    = Frame(self.root)
        self.mainFrame   = Frame(self.root)
        self.bottomFrame = Frame(self.root)
        
        self.tronFrame   = TronFrame(self.mainFrame) #, self.settings)
    
    def DrawUI(self):
        Grid.rowconfigure   (self.root, 0, weight=1)                                 # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.root, 0, weight=1)                                 # set weight=1 to authorize resizing element
        Grid.rowconfigure   (self.mainFrame, 0, weight=1, minsize=TronFrame.HEIGHT)  # set weight=1 to authorize resizing element
        Grid.columnconfigure(self.mainFrame, 0, weight=1, minsize=TronFrame.WIDTH)   # set weight=1 to authorize resizing element    

        self.topFrame.grid  (row=0, column=0)
        self.mainFrame.grid  (row=0, column=0)
        self.bottomFrame.grid(row=0, column=0)

class TronFrame:
    HEIGHT, WIDTH = 800, 800
    
    def __init__(self, root):
        self.root = root
        self.players = list()
        self.start_positions = dict()
        
        self.InitStartPositions()
        self.InitUI()
        self.DrawUI()
        self.InitPlayers()
        self.DrawGarages()

    def InitUI(self):
        self.canvas = Canvas(self.root, bd=2)
        #self.canvas.bind('<Key>', self.Start)
        
    def DrawUI(self):
        Grid.rowconfigure   (self.canvas, 0, weight=1, minsize=TronFrame.HEIGHT)  # set weight=1 to authorize resizing element in row[0] main.canvas
        Grid.columnconfigure(self.canvas, 0, weight=1, minsize=TronFrame.WIDTH)  # set weight=1 to authorize resizing element in column[0] main.canvas

        self.canvas.grid(row=0, column=0, sticky=E+S+W+N)
        self.canvas.focus_set()
        
    def InitPlayers(self):
        self.players.append("Pod1")
        self.pod1 = Pod( name       = "Joueur Rouge",
                            field      = self.canvas,
                            direction  = Pod.EAST, 
                            coord      = self.start_positions[Pod.WEST],
                            left       = "<Left>", 
                            right      = "<Right>",
                            boost      = "<Up>",
                            color      = "#FF0000",    #Red
                            outline    = "#990000" )
        self.players.append("Pod2")
        self.pod2 = Pod( name       = "Joueur Vert",
                            field      = self.canvas,
                            direction  = Pod.WEST, 
                            coord      = self.start_positions[Pod.EAST],
                            left       = "q", 
                            right      = "d",
                            boost      = "z",
                            color      = "#33CC33",    #Green
                            outline    = "#248F24" )
        self.players.append("Pod3")
        self.pod3 = Pod( name       = "Joueur Bleu",
                            field      = self.canvas,
                            direction  = Pod.SOUTH, 
                            coord      = self.start_positions[Pod.NORTH],
                            left       = "g", 
                            right      = "j",
                            boost      = "y",                             
                            color      = "#0099CC",    #Blue
                            outline    = "#00478F" )
        self.players.append("Pod4")
        self.pod4 = Pod( name       = "Joueur Orange",
                            field      = self.canvas,
                            direction  = Pod.NORTH, 
                            coord      = self.start_positions[Pod.SOUTH],
                            left       = "<KP_1>", 
                            right      = "<KP_3>",
                            boost      = "<KP_5>",                             
                            color      = "#FF9933",    #Orange
                            outline    = "#CC7A29" )

    def InitStartPositions(self):
        self.start_positions[Pod.WEST]  = {'x' : 20, 'y' : TronFrame.HEIGHT / 2  }
        self.start_positions[Pod.EAST]  = {'x' : TronFrame.WIDTH - 20 - Pod.THICKNESS - Pod.INTERVAL , 'y' : TronFrame.HEIGHT / 2  }
        self.start_positions[Pod.NORTH] = {'x' : TronFrame.WIDTH / 2,  'y' : 20  }
        self.start_positions[Pod.SOUTH] = {'x' : TronFrame.WIDTH / 2,  'y' : TronFrame.HEIGHT - 20  - Pod.THICKNESS - Pod.INTERVAL }

    def Start(self, nb, event=None):
        if nb == 1:
            self.pod1.start()
        elif nb ==  2:
            self.pod1.start()
            self.pod2.start()
        elif nb == 3:
            self.pod1.start()
            self.pod2.start()
            self.pod3.start()
        elif nb == 4:
            self.pod1.start()
            self.pod2.start()
            self.pod3.start()
            self.pod4.start()
        else:
            return(False)
            
    def DrawGarages(self):
        directions = (Pod.EAST, Pod.NORTH, Pod.WEST, Pod.SOUTH)
        for d in directions:
            garage = Pod( "garage",
                          self.canvas,
                          direction = (d + 180) % 360,
                          coord = self.start_positions[d],
                          left = None,
                          right = None,
                          boost = None,
                          color = "#808080",
                          outline = "#1A1A1A" )
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
    DELAY = 0.1
    THICKNESS = 8
    INTERVAL = 2
    
    def __init__( self, 
                  name,
                  field,
                  direction, 
                  coord,
                  left, right, boost,
                  color, outline):
        
        threading.Thread.__init__(self)
        
        self.name      = name
        self.field     = field
        self.direction = direction
        self.interval  = Pod.INTERVAL
        self.thickness = Pod.THICKNESS
        self.x, self.y = coord['x'], coord['y'],
        self.left      = left,
        self.right     = right,
        self.boost     = boost,
        self.color     = color,
        self.outline   = outline,
        self.go        = True
        
        self.delay = Pod.DELAY
        self.ticks = 0
        
        self.field.bind(self.left,  lambda event, angle=Pod.LEFT : self.Turn(angle))
        self.field.bind(self.right, lambda event, angle=Pod.RIGHT: self.Turn(angle))
        self.field.bind(self.boost, self.Boost)

    
    def run(self):
        while self.go:
            if self.ticks > 0:
                self.ticks -= 1
                if self.ticks == 0:
                    self.EndBoost()
            
            if self.Collision():
                self.go = False
            self.Move()
            time.sleep(self.delay)
    
    def Collision(self):
        xoff = self.x + int((self.interval + self.thickness) * math.cos(math.radians(self.direction)))
        yoff = self.y + int((self.interval + self.thickness) * math.sin(math.radians(self.direction)))

        # test if Pod is out of Frame:
        if xoff < 0  or xoff + self.thickness > TronFrame.WIDTH  or yoff < 0 or yoff + self.thickness > TronFrame.HEIGHT:
            print("[%s] out of field, he is gameover" % self.name)
            return(True)
        
        # test if Pod crossed a track:
        elif self.field.find_overlapping(xoff, yoff, xoff + self.thickness, yoff + self.thickness):
            print("[%s] overlapped, he is gameover" % self.name)
            return(True)
        
        # else you're good to go:
        else:
            return(False)


    def Move(self, ghost=False):
        if ghost == False:
            self.field.create_rectangle( self.x, 
                                         self.y, 
                                         self.x + self.thickness, 
                                         self.y + self.thickness,
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
    
    TronApp = Tk()
    TronApp.title("Tron Clone")                                     # application title
    TronApp.geometry("%dx%d" % (TronFrame.WIDTH, TronFrame.HEIGHT)) # set window size
    TronApp.resizable(width=False, height=False)                    # unable window resizing
    
    tron = MainWindow(TronApp)                                       # init main application Frame inside App

    TronApp.mainloop()
