import os
import sys
from config import *
import random

# Player 
class User:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.time = 0
        self.level = 1

    def get_score(self):
        return self.score

    def get_lives(self):
        return self.lives

    def get_time(self):
        return self.time

    def get_level(self):
        return self.level               

    def dec_live_user(self):
        self.lives = self.lives - 1

    def lost_lives(self):
        self.lives = 1    

    def update_score(self , score):
        self.score = self.score + score 

    def set_run_time(self,time):
        self.time = time 
    
    def set_level(self, level):
        self.level = level

    def inc_level(self):
        self.level = self.level + 1

    def reset_score(self):
        self.score = 0

    def reset_attri(self):
        self.score = 0
        self.lives = 3
        self.time = 0
        self.level = 1                      


# Board
class Board:
    def __init__(self):
        self.x_pos = x_screen_end - 3
        self.y_pos = ( y_screen_start + y_screen_end ) / 2
        self.length = 5
        self.speed = 1
        self.x_pos_prev = x_screen_end - 3
        self.y_pos_prev = ( y_screen_start + y_screen_end ) / 2
        self.length_prev = 5
        self.activate_shoot = 0

    def get_xpos(self):
        return self.x_pos

    def get_ypos(self):
        return self.y_pos

    def get_xposprev(self):
        return self.x_pos_prev

    def get_yposprev(self):
        return self.y_pos_prev

    def get_length(self):
        return self.length

    def get_lengthprev(self):
        return self.length_prev

    def get_speed(self):
        return self.speed

    def get_activateshoot(self):
        return self.activate_shoot                            

    def move_board(self , dir):
        if dir == 1:
            if (self.y_pos + self.speed + (self.length / 2)) <= y_screen_end - 50:
                self.x_pos_prev = self.x_pos
                self.y_pos_prev = self.y_pos
                self.y_pos = self.y_pos + self.speed

        else:
            if (self.y_pos - self.speed - (self.length/2)) >= y_screen_start + 50:
                self.x_pos_prev = self.x_pos
                self.y_pos_prev = self.y_pos
                self.y_pos = self.y_pos - self.speed       

    def inc_speed_board(self , speed):
        self.speed = speed

    def inc_length_board(self):
        self.length = 2*self.length
        self.length_prev = self.length

    def dec_length_board(self):
        if self.length > 1:
            self.length = int(self.length / 2)
            self.length_prev = self.length

    def activate_blasters(self):
        self.activate_shoot = 1

    def deactivate_blasters(self):
        self.activate_shoot = 0                    

# ball
class Ball:
    def __init__(self):
        self.x_pos = x_screen_end - 4
        self.y_pos = ( y_screen_start + y_screen_end ) / 2
        self.x_pos_prev = x_screen_end - 4
        self.y_pos_prev = ( y_screen_start + y_screen_end ) / 2
        self.x_speed = 1
        self.y_speed = 1
        self.lives = 3
        self.super_strength = 0
        self.together = 0

    def get_xpos(self):
        return self.x_pos

    def get_ypos(self):
        return self.y_pos

    def get_xposprev(self):
        return self.x_pos_prev

    def get_yposprev(self):
        return self.y_pos_prev

    def get_xspeed(self):
        return self.x_speed

    def get_yspeed(self):
        return self.y_speed

    def get_lives(self):
        return self.lives

    def get_superstrength(self):
        return self.super_strength

    def get_together(self):
        return self.together                 
    
    def change_yspeed(self):
        self.y_speed = -1 * self.y_speed

    def change_xspeed(self):
        self.x_speed = -1 * self.x_speed 

    def change_yspeedbyvalue(self,value):
        self.y_speed = value        
    
    def change_together_status(self , status):
        self.together = status    

    def move_ball(self , dir):
        if dir == 1:
            if (self.y_pos + 1 ) <= y_screen_end - 52:
                self.x_pos_prev = self.x_pos
                self.y_pos_prev = self.y_pos
                self.y_pos = self.y_pos + 1

        else:
            if (self.y_pos - 1) >= y_screen_start + 52:
                self.x_pos_prev = self.x_pos
                self.y_pos_prev = self.y_pos
                self.y_pos = self.y_pos - 1  

    def set_initial_speed(self):
        x_temp = (x_screen_start + x_screen_end) / 2
        y_temp = (y_screen_start + y_screen_end) / 2
        if self.y_pos == y_temp:
            self.x_speed = -1
            self.y_speed = 0
        else:
            self.x_speed = -1
            if y_temp > self.y_pos:
                self.y_speed = 1

            else:
                self.y_speed = -1

    def move_ball_speed(self):
        self.x_pos_prev = self.x_pos
        self.y_pos_prev = self.y_pos
        self.x_pos = self.x_pos + self.x_speed
        self.y_pos = self.y_pos + self.y_speed

    def update_live(self , live):
        if live == 0:
            self.lives = 3
        else:
            self.lives = live

    def inc_speed_ball(self):
        self.x_speed = self.x_speed
        self.y_speed = 2 * self.y_speed

    def dec_xpos(self):
        self.x_pos = self.x_pos - 1    

    def dec_speed_ball(self):
        if self.y_speed > 1:
            self.y_speed = int(self.y_speed)     

    def update_super_strength(self , super_strength):
        self.super_strength = super_strength

    def update_config(self , ball):
        self.x_pos = ball.x_pos
        self.y_pos = ball.y_pos
        self.x_pos_prev = ball.x_pos_prev
        self.y_pos_prev = ball.y_pos_prev
        self.lives = ball.lives
        self.super_strength = ball.super_strength
        self.together = ball.together
        self.x_speed = -1 * ball.x_speed
        self.y_speed =  -1 * ball.y_speed

    def lost_lives(self):
        self.lives = 0                                                           

# Brick
class Brick:
    def __init__(self , x_start_pos , y_start_pos , x_end_pos, y_end_pos,strength , typeofdropdown , rainbow):
        self.x_start_pos = x_start_pos
        self.y_start_pos = y_start_pos
        self.x_end_pos = x_end_pos
        self.y_end_pos = y_end_pos
        self.strength = strength
        self.typeofdropdown = typeofdropdown
        self.rainbow = rainbow

    def get_xstartpos(self):
        return self.x_start_pos

    def get_xendpose(self):
        return self.x_end_pos

    def get_ystartpos(self):
        return self.y_start_pos

    def get_yendpose(self):
        return self.y_end_pos

    def get_strength(self):
        return self.strength

    def get_typeofdropdown(self):
        return self.typeofdropdown

    def get_rainbow(self):
        return self.rainbow                        

class Fixed_Brick(Brick):
    def __init__(self , x_start_pos , y_start_pos , x_end_pos, y_end_pos):
        super().__init__(x_start_pos , y_start_pos , x_end_pos, y_end_pos, 100 , 0 , 0)

    def dec_str(self):
        self.strength = 0

    def dec_pos(self):
        self.x_start_pos = self.x_start_pos + 1
        self.x_end_pos = self.x_end_pos + 1        

class Dynamic_Brick(Brick):
    def __init__(self , x_start_pos , y_start_pos , x_end_pos, y_end_pos, strength, typeofdropdown , rainbow):
        super().__init__(x_start_pos , y_start_pos , x_end_pos, y_end_pos, strength, typeofdropdown , rainbow)

    def dec_str(self , destroy):
        if destroy == 1:
            self.strength = 0
        else:
            self.strength = self.strength - 1

    def dec_pos(self):
        self.x_start_pos = self.x_start_pos + 1
        self.x_end_pos = self.x_end_pos + 1

    def change_strength(self,strength):
        self.strength = strength

    def change_rainbow(self):
        self.rainbow = 0


class BossEnemy:
    def __init__(self , x_pos_start , y_pos_start , x_pos_end , y_pos_end):
        self.x_pos_start = x_pos_start
        self.y_pos_start = y_pos_start
        self.x_pos_end = x_pos_end
        self.y_pos_end = y_pos_end
        self.x_pos_start_prev = x_pos_start
        self.y_pos_start_prev = y_pos_start
        self.x_pos_end_prev = x_pos_end
        self.y_pos_end_prev = y_pos_end
        self.speed = 1
        self.health = 100
        self.start_bombs = 0

    def get_xposstart(self):
        return self.x_pos_start

    def get_yposstart(self):
        return self.y_pos_start

    def get_xposstartprev(self):
        return self.x_pos_start_prev

    def get_yposstartprev(self):
        return self.y_pos_start_prev    

    def get_xposend(self):
        return self.x_pos_end

    def get_yposend(self):
        return self.y_pos_end

    def get_xposendprev(self):
        return self.x_pos_end_prev

    def get_yposendprev(self):
        return self.y_pos_end_prev    

    def get_health(self):
        return self.health

    def get_speed(self):
        return self.speed

    def get_startbombs(self):
        return self.start_bombs    

    def move_boss(self , dir):
        if dir == 1:
            if (self.y_pos_end + self.speed) <= y_screen_end - 50:
                self.x_pos_start_prev = self.x_pos_start
                self.y_pos_start_prev = self.y_pos_start
                self.x_pos_end_prev = self.x_pos_end
                self.y_pos_end_prev = self.y_pos_end
                self.y_pos_start = self.y_pos_start + self.speed
                self.y_pos_end = self.y_pos_end + self.speed

        else:
            if (self.y_pos_start - self.speed) >= y_screen_start + 50:
                self.x_pos_start_prev = self.x_pos_start
                self.y_pos_start_prev = self.y_pos_start
                self.x_pos_end_prev = self.x_pos_end
                self.y_pos_end_prev = self.y_pos_end
                self.y_pos_start = self.y_pos_start - self.speed
                self.y_pos_end = self.y_pos_end - self.speed 

    def inc_speed_boss(self , speed):
        self.speed = speed

    def start_bombing(self):
        self.start_bombs = 1

    def dec_health(self):
        self.health = self.health - 10                                           