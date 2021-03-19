import os
import sys

class Bomb:
    def __init__(self, x_pos , y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def move_bomb(self):
        self.x_pos = self.x_pos + 1

    def get_xpos(self):
        return self.x_pos

    def get_ypos(self):
        return self.y_pos            