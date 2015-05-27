from tkinter import *
from tkinter import ttk
import math

EAST  = 0
NORTH = 90
WEST  = 180
SOUTH = 270

ANGLE = 90

DIRECTIONS = dict()
DIRECTIONS[EAST]  = math.radians(EAST)
DIRECTIONS[NORTH] = math.radians(NORTH)
DIRECTIONS[WEST]  = math.radians(WEST)
DIRECTIONS[SOUTH] = math.radians(SOUTH)

class Pod:
    def __init__(self, name, direction, speed, thickness):
        self.name = name
        self.direction = direction
        self.speed = speed
        self.thickness = thickness
        self.x, self.y = 0, 0

    def Move(self):
        self.x += int(self.speed * math.cos(DIRECTIONS[self.direction]))
        self.y += int(self.speed * math.sin(DIRECTIONS[self.direction]))
    
    def Turn(self, side):
        xOffset1 = -int(math.cos(DIRECTIONS[self.direction]))
        yOffset1 = -int(math.sin(DIRECTIONS[self.direction]))

        if   side == "LEFT":
            self.direction = (self.direction + ANGLE) % 360
        elif side == "RIGHT":
            self.direction = (self.direction - ANGLE) % 360
        else:
            return(false)
        
        xOffset2 = int(math.cos(DIRECTIONS[self.direction]))
        yOffset2 = int(math.sin(DIRECTIONS[self.direction]))

        # print("Turn %s, correction: %d %d" %(side, (xOffset1 + xOffset2) * math.ceil(self.thickness / 2), (yOffset1 + yOffset2) * math.ceil(self.thickness / 2)))

        self.x += (xOffset1 + xOffset2) * math.ceil(self.thickness / 2)
        self.y += (yOffset1 + yOffset2) * math.ceil(self.thickness / 2)
    
    def __str__(self):
        return("[%s] {%d:%d} speed: %d direction: %d" % (self.name, self.x, self.y, self.speed, self.direction))
        
if __name__ == "__main__":
    
    pod = Pod("Pod", EAST, 2, 5)
    print(pod)
    pod.Move()
    print(pod)
    pod.Turn("LEFT")
    pod.Move()
    print(pod)
    pod.Turn("LEFT")
    pod.Move()
    print(pod)
    pod.Turn("LEFT")
    pod.Move()
    print(pod)
    pod.Turn("LEFT")
    pod.Move()
    print(pod)
    pod.Move()
    print(pod)
    pod.Turn("RIGHT")
    pod.Move()
    print(pod)
