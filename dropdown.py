import os
import sys

class DropDown:
    def __init__(self , x_pos , y_pos , type_of_power):
        self.type_of_power = type_of_power
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_dropdown(self):
        self.x_pos = self.x_pos + 1    