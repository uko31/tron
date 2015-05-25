#!/usr/bin/python

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#   Things to do and ideas:
#    - déterminer le vainqueur!
#    - permettre des lignes plus grosses
#
#    - mettre en place un turbo avec recharge (speedx2 pendant X ticks)
#    - faire apparaitre les garages de départ
#    - mettre en place un team play (plusieurs joueurs contre 1)
#    - mettre en place la notion de longeur de trace (avec fade progressif)
#    - capture the flag
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
        
        self.InitStartPositions()
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

    def InitStartPositions(self):
        self.start_positions = dict()
        self.start_positions['West']  = {'x' : 10,           'y' : _HEIGHT_ / 2  }
        self.start_positions['East']  = {'x' : _WIDTH_ - 10, 'y' : _HEIGHT_ / 2  }
        self.start_positions['North'] = {'x' : _WIDTH_ / 2,  'y' : 10            }
        self.start_positions['South'] = {'x' : _WIDTH_ / 2,  'y' : _HEIGHT_ - 10 }

    def Start(self, event=None):
        if self.players.count("Player-%s" % event.char):
            return(False)
        
        if event.char == '1':
            self.players.append("Player-%c" % event.char)
            self.player1 = TronPlayer(self, "Player-1", self.start_positions['West'], self.speed, 0, '<Left>', '<Right>', 'blue')
            self.player1.start()
        if event.char == '2':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self, "Player-2", self.start_positions['East'], -self.speed, 0, 'a', 'z', 'red')
            self.player2.start()
        if event.char == '3':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self, "Player-3", self.start_positions['North'], 0, self.speed, 'y', 'u', 'green')
            self.player2.start()
        if event.char == '4':
            self.players.append("Player-%c" % event.char)
            self.player2 = TronPlayer(self, "Player-4", self.start_positions['South'], 0, -self.speed, ':', '!', 'cyan')
            self.player2.start()

class TronPlayer(threading.Thread):
    
    def __init__(self, root, name, coord, x_speed, y_speed, left_key, right_key, color):
        threading.Thread.__init__(self)
        
        self.canvas = root.canvas
        self.name = name
        self.x = coord['x']
        self.y = coord['y']
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
        while not self.terminate:
            if self.collision():
                self.canvas.create_line(self.x, self.y, self.x + self.x_speed, self.y + self.y_speed, fill = self.color, width = self.width)
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
            
            if self.x < 0  or self.x > _WIDTH_  or self.y < 0 or self.y > _HEIGHT_:
                print("[%s] out of field, he is gameover" % self.name)
                return(True)
            elif self.canvas.find_overlapping(xoff1, yoff1, xoff2, yoff2):
                print("[%s] overlapped, he is gameover" % self.name)
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