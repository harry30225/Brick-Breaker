import os
import sys
from config import *
from colorama import Fore, Back , Style
import random


# Print at desired position
def print_there(x, y, text):
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
    sys.stdout.flush()

class Game_Screen:
    def __init__(self):
        self.x_map_begin = x_screen_start
        self.x_map_end = x_screen_end
        self.y_map_begin = y_screen_start + 50
        self.y_map_end = y_screen_end - 50

    def PrintHeader(self , player):
        print_there(6, 4, 'Score : ' + str(player.score))
        print_there(6 , (y_screen_start + y_screen_end ) / 2 , 'Time : ' + str(player.time))
        print_there(4 , (y_screen_start + y_screen_end ) / 2 , 'BRICK BREAKER')
        print_there(6 , y_screen_end - 8 , 'Lives : ' + str(player.lives))
        print_there(8,(y_screen_start + y_screen_end)/2 , 'Level : ' + str(player.level))
        for i in range(y_screen_end - y_screen_start + 1):
            print_there(12, i+3, 'X')

    def PrintBoundary(self):
        #Upper and Lower Boundary
        for i in range(self.y_map_begin , self.y_map_end + 1):
            print_there(self.x_map_begin , i , Fore.WHITE + '!' + Style.RESET_ALL)
            print_there(self.x_map_end , i , Fore.WHITE + '!' + Style.RESET_ALL) 
        # Left and Right Boundary
        for i in range(self.x_map_begin , self.x_map_end + 1):
            print_there(i , self.y_map_begin ,Fore.WHITE + '!' + Style.RESET_ALL)
            print_there(i , self.y_map_end ,Fore.WHITE + '!' + Style.RESET_ALL)       

    def PrintBall(self , ball):
        print_there(ball.x_pos_prev, ball.y_pos_prev, ' ')
        if ball.super_strength == 0:
            print_there(ball.x_pos , ball.y_pos, Fore.CYAN + '*' + Style.RESET_ALL)

        else:
            print_there(ball.x_pos , ball.y_pos ,Fore.RED + '*' + Style.RESET_ALL)    

    def PrintBoard(self, board):
        for i in range(board.length_prev):
            print_there(board.x_pos_prev , board.y_pos_prev + ( i - (board.length / 2)), ' ')
        for i in range(board.length):
            print_there(board.x_pos , board.y_pos + ( i - (board.length / 2)), '=')

        if board.activate_shoot == 1:
            print_there(board.x_pos_prev - 1 , board.y_pos_prev + (0 - (board.length/2)) , ' ')
            print_there(board.x_pos_prev - 1 , board.y_pos_prev + (board.length_prev - 1 - (board.length/2)) , ' ')
            print_there(board.x_pos - 1 , board.y_pos + (0 - (board.length/2)) ,Fore.RED +  '!' + Style.RESET_ALL)
            print_there(board.x_pos - 1 , board.y_pos + (board.length - 1 - (board.length/2)) , Fore.RED + '!' + Style.RESET_ALL)    

    def PrintBricks(self , fixed_bricks , dynamic_bricks):
        for fix_brick in fixed_bricks:
            if fix_brick.strength == 100:
                print_there(fix_brick.x_start_pos, fix_brick.y_start_pos , '|')
                print_there(fix_brick.x_start_pos, fix_brick.y_end_pos , '|')

            else:
                print_there(fix_brick.x_start_pos, fix_brick.y_start_pos , ' ')
                print_there(fix_brick.x_start_pos, fix_brick.y_end_pos , ' ')

        for dynamic_brick in dynamic_bricks:
            if dynamic_brick.rainbow == 1:
                dynamic_brick.change_strength(random.randint(1,3))
            if dynamic_brick.strength == 1:
                print_there(dynamic_brick.x_start_pos, dynamic_brick.y_start_pos , Fore.YELLOW + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.x_end_pos, dynamic_brick.y_end_pos , Fore.YELLOW + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 2:
                print_there(dynamic_brick.x_start_pos, dynamic_brick.y_start_pos , Fore.BLUE + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.x_end_pos, dynamic_brick.y_end_pos , Fore.BLUE + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 3:
                print_there(dynamic_brick.x_start_pos, dynamic_brick.y_start_pos , Fore.RED + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.x_end_pos, dynamic_brick.y_end_pos , Fore.RED + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 0:
                print_there(dynamic_brick.x_start_pos, dynamic_brick.y_start_pos , ' ')
                print_there(dynamic_brick.x_end_pos, dynamic_brick.y_end_pos , ' ')

    def PrintClearBricks(self,fixed_bricks,dynamic_bricks):
        for fix_brick in fixed_bricks:
            print_there(fix_brick.x_start_pos, fix_brick.y_start_pos , ' ')
            print_there(fix_brick.x_start_pos, fix_brick.y_end_pos , ' ')

        for dynamic_brick in dynamic_bricks:
            print_there(dynamic_brick.x_start_pos, dynamic_brick.y_start_pos , ' ')
            print_there(dynamic_brick.x_end_pos, dynamic_brick.y_end_pos , ' ')



    def PrintDropDowns(self , dropdowns):
        for dropdown in dropdowns:
            print_there(dropdown.x_pos_prev , dropdown.y_pos_prev , '    ')
            if dropdown.type_of_power == 1:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.BLUE + '[+]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 2:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.RED + '[-]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 3:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.YELLOW + '[**]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 4:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.CYAN + '[+*]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 5:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.LIGHTRED_EX + '[O]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 6:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.WHITE + '[_*]' + Style.RESET_ALL)

            elif dropdown.type_of_power == 7:
                print_there(dropdown.x_pos , dropdown.y_pos , Fore.LIGHTGREEN_EX + '[!!]' + Style.RESET_ALL)      

            if dropdown.gravity != 0:
                dropdown.change_gravity()

    def PrintBlasters(self, blasters):
        for blaster in blasters:
            print_there(blaster.x_pos + 1, blaster.y_pos , ' ')
            print_there(blaster.x_pos , blaster.y_pos , Fore.LIGHTBLUE_EX + '|' + Style.RESET_ALL)                                              

    def PrintRestartGameLost(self , player , ball):
        print_there((x_screen_end + x_screen_start)/2 , (y_screen_start + y_screen_end ) / 2 , Fore.MAGENTA + 'Balls Left: ' + str(ball.lives) + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start)/2 + 2 , (y_screen_start + y_screen_end ) / 2 , Fore.CYAN + 'Lives Left: ' + str(player.lives - 1) + Style.RESET_ALL)   

        if ball.lives == 0 and player.lives > 1:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Life Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)

        elif ball.lives > 0:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Ball Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)

        elif player.lives == 1:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Game Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)
    
    def PrintRestartGameWon(self , player):
        print_there((x_screen_end + x_screen_start) / 2 , (y_screen_end + y_screen_start) / 2 , Fore.BLUE + 'You Have Won !!!' + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 2 , (y_screen_end + y_screen_start) / 2 , Fore.MAGENTA + 'Score : ' + str(player.score) + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 4 , (y_screen_end + y_screen_start) / 2 , Fore.WHITE + 'Time Taken : ' + str(player.time) + Style.RESET_ALL)
        if player.level < 3:
            print_there((x_screen_end + x_screen_start) / 2 + 6 , (y_screen_end + y_screen_start) / 2 , Fore.YELLOW + 'Start Next Level Press h' + Style.RESET_ALL)

        if player.level == 3:    
            print_there((x_screen_end + x_screen_start) / 2 + 6 , (y_screen_end + y_screen_start) / 2 , Fore.YELLOW + 'Start New Game Press h' + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 8 , (y_screen_end + y_screen_start) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)