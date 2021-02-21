import os
import sys

class GameOver:
    def gameLost(self, ball , game_screen):
        if ball.x_pos >= game_screen.x_map_end:
            ball.lives = ball.lives - 1
            return 1

        return 0 

    def gameWon(self, total_brick_destroyed , no_of_bricks):
        return total_brick_destroyed == no_of_bricks       