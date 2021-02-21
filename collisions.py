import os
import sys

class Collision:
    def Collision_ball_wall(self, ball , game_screen):
        # upper collision
        if (ball.x_pos_prev >= game_screen.x_map_begin) and (ball.x_pos <= game_screen.x_map_begin):
            ball.x_speed = -1 * ball.x_speed

        # Left collision and Right collision
        if ((ball.y_pos_prev >= game_screen.y_map_begin) and (ball.y_pos <= game_screen.y_map_begin)) or ((ball.y_pos_prev <= game_screen.y_map_end) and (ball.y_pos >= game_screen.y_map_end)):
            ball.y_speed = -1 * ball.y_speed

    def Collision_ball_board(self , ball , board):
        if ball.y_pos >= board.y_pos - (board.length)/2 and ball.y_pos <= board.y_pos + (board.length)/2:
            ball.x_speed = -1 * ball.x_speed
            if ball.y_speed > 0:
                ball.y_speed = abs((abs(ball.y_pos - board.y_pos) + 1) * ball.x_speed)

            else:
                ball.y_speed = -1 * abs((abs(ball.y_pos - board.y_pos) + 1) * ball.x_speed)

            return 1

        return 0        

    def Collision_ball_fixed_brick(self ,ball , fixed_brick):
        # upper and downward collision
        ball.x_speed = -1*ball.x_speed
        if ball.super_strength == 100:
            fixed_brick.dec_str()
        # left and right collision

    def Collision_ball_dynamic_brick(self ,ball , dynamic_brick):
        # upper and downward collision
        ball.x_speed = -1*ball.x_speed
        if ball.super_strength == 100:
            dynamic_brick.dec_str(1)

        else:    
            dynamic_brick.dec_str(0)
        # left and right collision  

    def Collision_board_dropdown(self, board, dropdown):
        if dropdown.x_pos == board.x_pos and dropdown.y_pos >= board.y_pos - (board.length)/2 and dropdown.y_pos <= board.y_pos + (board.length)/2:
            return 1

        return 0

    def Collision_dropdown_wall(self , dropdown , x_map_end):
        if x_map_end == dropdown.x_pos:
            return 1

        return 0    
        
