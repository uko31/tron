#!/usr/bin/python

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Things to do and ideas:
#    - déterminer le vainqueur!
#    - permettre des lignes plus grosses
#
#    - mettre en place un turbo avec recharge (speedx2 pendant X ticks)
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

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
_THICK_  = 6
_DELAY_  = 0.02

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Classes
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

class TronFrame:
    
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

    def Start(self, event=None):
        if self.players.count("Player-%s" % event.char):
            return(False)
        
        if event.char == '1':
            self.players.append("Player-%c" % event.char)
            self.player1 = TronPlayer(self.canvas, "Player-1", 10, 250, self.speed, 0, '<Right>', '<Left>', 'blue')
            self.player1.start()
        if event.char == '2':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self.canvas, "Player-2", 250, 10, 0, self.speed, 'z', 'a', 'red')
            self.player2.start()
        if event.char == '3':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self.canvas, "Player-3", 490, 250, -self.speed, 0, 'u', 'y', 'green')
            self.player2.start()
        if event.char == '4':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self.canvas, "Player-4", 250, 490, 0, -self.speed, '!', '/', 'cyan')
            self.player2.start()

class TronPlayer(threading.Thread):
    
    def __init__(self, canvas, name, x, y, x_speed, y_speed, right_key, left_key, color):
        threading.Thread.__init__(self)
        
        self.canvas = canvas
        self.name = name
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.delay = _DELAY_
        self.terminate = False
        self.color = color
        
        self.width = _THICK_
        
        self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill = self.color, width = self.width)
        self.x, self.y = self.x + self.x_speed, self.y + self.y_speed
        self.canvas.bind(left_key, self.turnLeft)
        self.canvas.bind(right_key, self.turnRight)
        
    def run(self):
        while (self.x < 500 and self.y < 500 and self.x > 0 and self.y > 0) and not self.terminate:
            if self.collision():
                self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill = self.color, width = self.width)
                print("[%s] overlapped, he is gameover" % self.name)
                self.terminate = True
                
            self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill = self.color, width = self.width)
            self.x, self.y = self.x + self.x_speed, self.y + self.y_speed
            time.sleep(self.delay)
    
    def collision(self):
            if   self.x_speed > 0:
                xoff1 = self.x + 1 
                yoff1 = self.y - self.width/2
                xoff2 = self.x + self.x_speed
                yoff2 = self.y + self.width/2
            elif self.x_speed < 0:
                xoff1 = self.x - 1
                yoff1 = self.y - self.width/2
                xoff2 = self.x + self.x_speed
                yoff2 = self.y + self.width/2
            elif self.y_speed > 0:
                xoff1 = self.x - self.width/2
                yoff1 = self.y + 1
                xoff2 = self.x + self.width/2
                yoff2 = self.y + self.y_speed
            elif self.y_speed < 0:
                xoff1 = self.x - self.width/2
                yoff1 = self.y - 1
                xoff2 = self.x + self.width/2
                yoff2 = self.y + self.y_speed
            
            if self.canvas.find_overlapping(xoff1, yoff1, xoff2, yoff2):
                return(True)
            else:
                return(False)
    
    def turnLeft(self, event=None):
        if ( self.x_speed != 0 ):
            if self.x_speed > 0:
                self.x -= self.width / 2
                self.y -= self.width / 2
            else:
                self.x += self.width / 2
                self.y += self.width / 2
                
            self.y_speed -= self.x_speed
            self.x_speed = 0
            
        elif ( self.y_speed != 0 ):
            if self.y_speed > 0:
                self.x += self.width / 2
                self.y -= self.width / 2
            else:
                self.x -= self.width / 2
                self.y += self.width / 2

            self.x_speed += self.y_speed
            self.y_speed = 0

    def turnRight(self, event=None):
        if   ( self.x_speed != 0 ):
            if self.x_speed > 0:
                self.x -= self.width / 2
                self.y += self.width / 2
            else:
                self.x += self.width / 2
                self.y -= self.width / 2

            self.y_speed += self.x_speed
            self.x_speed = 0
            
        elif ( self.y_speed != 0 ):
            if self.y_speed > 0:
                self.x -= self.width / 2
                self.y -= self.width / 2
            else:
                self.x += self.width / 2
                self.y += self.width / 2

            self.x_speed -= self.y_speed
            self.y_speed = 0


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Main Program
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

if __name__ == "__main__":

    TronApp = Tk()                                      # init application
    TronApp.title("Tron Clone")                         # application title
    TronApp.geometry("%dx%d" % (_WIDTH_, _HEIGHT_))     # set window size
    TronApp.resizable(width=False, height=False)        # unable window resizing
    
    tron = TronFrame(TronApp, _SPEED_)                  # init main application Frame inside App
    
    TronApp.mainloop()                                  # main loop