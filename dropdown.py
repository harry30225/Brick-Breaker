import os
import sys

class DropDown:
    def __init__(self , x_pos , y_pos , type_of_power , x_speed,y_speed , gravity):
        self.type_of_power = type_of_power
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity = gravity
        self.x_pos_prev = x_pos
        self.y_pos_prev = y_pos

    def move_dropdown(self):
        self.x_pos_prev = self.x_pos
        self.y_pos_prev = self.y_pos
        self.x_pos = self.x_pos + self.x_speed
        self.y_pos = self.y_pos + self.y_speed

    def change_gravity(self):
        self.gravity = (self.gravity + 1)
        if self.gravity < 0:
            if int(self.x_speed/2) > 0:
                self.x_speed = int(self.x_speed / 2)
            if self.gravity == -1:
                self.x_speed = 0    
        if self.gravity == 0:
            self.x_speed = 1
            self.y_speed = self.y_speed
            

    def change_xspeed(self):
        self.x_speed = -1 * self.x_speed

    def change_yspeed(self):
        self.y_speed = -1 * self.y_speed               