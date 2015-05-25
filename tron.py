#!/usr/bin/python

from tkinter import *

import time
import threading

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Program Configuration Variables
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

_SPEED_  = 1
_HEIGHT_ = 500
_WIDTH_  = 500

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Classes
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class SnakeFrame:
    
    def __init__(self, root, speed):
        self.root = root
        self.speed = speed
        self.players = list()
        
        self.InitUI()
        self.DrawUI()
        
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

        print(self.canvas.winfo_width())

    def DrawLine(self, event):
        self.canvas.create_line(self.x, self.y, event.x, event.y)
        self.x, self.y = event.x, event.y
        
    def Start(self, event=None):
        if self.players.count("Player-%c" % event.char):
            return(False)
        
        if event.char == '1':
            self.players.append("Player-%c" % event.char)
            self.player1 = SnakePlayer(self.canvas, "Player-1", 10, 250, self.speed, 0, '<Right>', '<Left>', 'blue')
            self.player1.start()
        if event.char == '2':
            self.players.append("Player-%c" % event.char)
            self.player2 = SnakePlayer(self.canvas, "Player-2", 250, 10, 0, self.speed, 'z', 'a', 'red')
            self.player2.start()
        if event.char == '3':
            self.players.append("Player-%c" % event.char)
            self.player2 = SnakePlayer(self.canvas, "Player-3", 490, 250, -self.speed, 0, 'u', 'y', 'green')
            self.player2.start()
        if event.char == '4':
            self.players.append("Player-%c" % event.char)
            self.player2 = SnakePlayer(self.canvas, "Player-4", 250, 490, 0, -self.speed, '!', '/', 'cyan')
            self.player2.start()

class SnakePlayer(threading.Thread):
    
    def __init__(self, canvas, name, x, y, x_speed, y_speed, right_key, left_key, color):
        threading.Thread.__init__(self)
        
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.delay = 0.02
        self.terminate = False
        self.color = color
        
        self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill=self.color)
        self.x, self.y = self.x + self.x_speed, self.y + self.y_speed
        self.canvas.bind(left_key, self.turnLeft)
        self.canvas.bind(right_key, self.turnRight)
        
    def run(self):
        while (self.x < 500 and self.y < 500 and self.x > 0 and self.y > 0) and not self.terminate:
            # Gestion de la collision:
            if self.canvas.find_overlapping(self.x + self.x_speed, self.y + self.y_speed, 
                                            self.x + 2*self.x_speed, self.y + 2*self.y_speed):
                print("[%s] overlapped, he is gameover" % self.name)
                self.terminate = True
            
            self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill=self.color)
            self.x, self.y = self.x + self.x_speed, self.y + self.y_speed
            time.sleep(self.delay)
    
    def turnLeft(self, event=None):
        if   ( self.x_speed != 0 ):
            self.y_speed -= self.x_speed
            self.x_speed = 0
            
        elif ( self.y_speed != 0 ):
            self.x_speed += self.y_speed
            self.y_speed = 0

    def turnRight(self, event=None):
        if   ( self.x_speed != 0 ):
            self.y_speed += self.x_speed
            self.x_speed = 0
            
        elif ( self.y_speed != 0 ):
            self.x_speed -= self.y_speed
            self.y_speed = 0


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Main Program
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if __name__ == "__main__":

    SnakeApp = Tk()                 # init application
    SnakeApp.title("Snake")         # application title
    SnakeApp.geometry("%dx%d" % (_WIDTH_, _HEIGHT_))
    SnakeApp.resizable(width=False, height=False)
    
    snake = SnakeFrame(SnakeApp, _SPEED_)    # init main application Frame inside App
    
    SnakeApp.mainloop()             # main loop