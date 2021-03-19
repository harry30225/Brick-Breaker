import os
import sys

class Collision:
    def Collision_ball_wall(self, ball , game_screen):
        # upper collision
        if (ball.get_xposprev() >= game_screen.get_xmapbegin()) and (ball.x_pos <= game_screen.get_xmapbegin()):
            ball.x_speed = -1 * ball.x_speed

        # Left collision and Right collision
        if ((ball.get_yposprev() >= game_screen.get_ymapbegin()) and (ball.get_ypos() <= game_screen.get_ymapbegin())) or ((ball.get_yposprev() <= game_screen.get_ymapend()) and (ball.get_ypos() >= game_screen.get_ymapend())):
            ball.change_yspeed()

    def Collision_ball_board(self , ball , board):
        if ball.get_ypos() >= board.get_ypos() - (board.get_length())/2 and ball.get_ypos() <= board.get_ypos() + (board.get_length())/2:
            ball.change_xspeed()
            if ball.get_yspeed() > 0:
                ball.change_yspeedbyvalue(abs((abs(ball.get_ypos() - board.get_ypos()) + 1) * ball.get_xspeed()))

            else:
                ball.change_yspeedbyvalue(-1 * abs((abs(ball.get_ypos() - board.get_ypos()) + 1) * ball.get_xspeed()))

            return 1

        return 0        

    def Collision_ball_fixed_brick(self ,ball , fixed_brick):
        # upper and downward collision
        ball.change_xspeed()
        if ball.get_superstrength() == 100:
            fixed_brick.dec_str()
        # left and right collision

    def Collision_ball_dynamic_brick(self ,ball , dynamic_brick):
        # upper and downward collision
        ball.change_xspeed()
        if ball.get_superstrength() == 100:
            dynamic_brick.dec_str(1)

        else:    
            dynamic_brick.dec_str(0)
        # left and right collision

    def Collision_ball_bossenemy(self , ball , bossenemy):
        # Downward collision
        if ball.get_xpos() == bossenemy.get_xposend() and (ball.get_ypos() >= bossenemy.get_yposstart() and ball.get_ypos() <= bossenemy.get_yposend()):
            ball.change_xspeed()
            return 1
        # left and right collision
        if (ball.get_xpos() >= bossenemy.get_xposstart() and ball.get_xpos() <= bossenemy.get_xposend()) and (ball.get_ypos() == bossenemy.get_yposstart() or ball.get_ypos() == bossenemy.get_yposend()):
            ball.change_yspeed()
            return 1

        return 0        
  

    def Collision_board_dropdown(self, board, dropdown):
        if dropdown.get_xpos() == board.get_xpos() and dropdown.get_ypos() >= board.get_ypos() - (board.get_length())/2 and dropdown.get_ypos() <= board.get_ypos() + (board.get_length())/2:
            return 1

        return 0

    def Collision_dropdown_wall(self , dropdown , x_map_end):
        if x_map_end <= dropdown.get_xpos() and x_map_end >= dropdown.get_xposprev():
            return 1

        return 0

    def Collision_dropdown_sidewalls(self, dropdown , x_map_begin , y_map_begin , y_map_end):
        # upper collision
        if (dropdown.get_xpos() <= x_map_begin) and (dropdown.get_xposprev() >= x_map_begin):
            dropdown.change_xspeed()

        # left right collsion
        if ((dropdown.get_ypos() <= y_map_begin) and (dropdown.get_yposprev() >= y_map_begin)) or ((dropdown.get_ypos() >= y_map_end) and (dropdown.get_yposprev() <= y_map_end)):
            dropdown.change_yspeed()

    def Collision_bomb_lowerwall(self , bomb , x_map_end):
        if (bomb.get_xpos() >= x_map_end) and (bomb.get_xpos() - 1 <= x_map_end):
            return 1

        return 0

    def Collision_bomb_board(self , bomb , board):
        if bomb.get_xpos() >= board.get_xpos() and bomb.get_xpos() - 1 <= board.get_xpos() and bomb.get_ypos() >= board.get_ypos() - (board.get_length())/2 and bomb.get_ypos() <= board.get_ypos() + (board.get_length())/2:
            return 1

        return 0                

        
