import os
import sys

class Blaster:
    def __init__(self , x_pos , y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_blaster(self):
        self.x_pos = self.x_pos - 1    