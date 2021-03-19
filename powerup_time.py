import os
import sys

class PowerupTime:
    def __init__(self):
        self.start_time = 0
        self.total_time = 0

    def get_starttime(self):
        return self.start_time

    def get_totaltime(self):
        return self.total_time

    def update_starttime(self,time):
        self.start_time = time

    def update_totaltime(self , time):
        self.total_time = self.total_time + time

    def reset_totaltime(self):
        self.total_time = 0                    