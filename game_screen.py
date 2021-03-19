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

    def get_xmapbegin(self):
        return self.x_map_begin

    def get_xmapend(self):
        return self.x_map_end

    def get_ymapbegin(self):
        return self.y_map_begin

    def get_ymapend(self):
        return self.y_map_end            

    def PrintHeader(self , player):
        print_there(6, 4, 'Score : ' + str(player.get_score()))
        print_there(6 , (y_screen_start + y_screen_end ) / 2 , 'Time : ' + str(player.get_time()))
        print_there(4 , (y_screen_start + y_screen_end ) / 2 , 'BRICK BREAKER')
        print_there(6 , y_screen_end - 8 , 'Lives : ' + str(player.get_lives()))
        print_there(8,(y_screen_start + y_screen_end)/2 , 'Level : ' + str(player.get_level()))
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
        for i in range(board.get_lengthprev()):
            print_there(board.get_xposprev() , board.get_yposprev() + ( i - (board.get_length() / 2)), ' ')
        for i in range(board.get_length()):
            print_there(board.get_xpos() , board.get_ypos() + ( i - (board.get_length() / 2)), '=')

        if board.activate_shoot == 1:
            print_there(board.get_xposprev() - 1 , board.get_yposprev() + (0 - (board.get_length()/2)) , ' ')
            print_there(board.get_xposprev() - 1 , board.get_yposprev() + (board.get_lengthprev() - 1 - (board.get_length()/2)) , ' ')
            print_there(board.get_xpos() - 1 , board.get_ypos() + (0 - (board.get_length()/2)) ,Fore.RED +  '!' + Style.RESET_ALL)
            print_there(board.get_xpos() - 1 , board.get_ypos() + (board.get_length() - 1 - (board.get_length()/2)) , Fore.RED + '!' + Style.RESET_ALL)    

    def PrintBricks(self , fixed_bricks , dynamic_bricks):
        for fix_brick in fixed_bricks:
            if fix_brick.get_strength() == 100:
                print_there(fix_brick.get_xstartpos(), fix_brick.get_ystartpos() , '|')
                print_there(fix_brick.get_xstartpos(), fix_brick.get_yendpose() , '|')

            else:
                print_there(fix_brick.get_xstartpos(), fix_brick.get_ystartpos() , ' ')
                print_there(fix_brick.get_xstartpos(), fix_brick.get_yendpose() , ' ')

        for dynamic_brick in dynamic_bricks:
            if dynamic_brick.get_rainbow() == 1:
                dynamic_brick.change_strength(random.randint(1,3))
            if dynamic_brick.get_strength() == 1:
                print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.YELLOW + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.YELLOW + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 2:
                print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.BLUE + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.BLUE + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 3:
                print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.RED + '|' + Style.RESET_ALL)
                print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.RED + '|' + Style.RESET_ALL)

            elif dynamic_brick.strength == 0:
                print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , ' ')
                print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , ' ')

    def PrintDefensiveLayer(self , health , defensive_bricks):
        if int(health) <= 40:
            for dynamic_brick in defensive_bricks:
                if dynamic_brick.get_rainbow() == 1:
                    dynamic_brick.change_strength(random.randint(1,3))
                if dynamic_brick.get_strength() == 1:
                    print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.YELLOW + '|' + Style.RESET_ALL)
                    print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.YELLOW + '|' + Style.RESET_ALL)
    
                elif dynamic_brick.strength == 2:
                    print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.BLUE + '|' + Style.RESET_ALL)
                    print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.BLUE + '|' + Style.RESET_ALL)
    
                elif dynamic_brick.strength == 3:
                    print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , Fore.RED + '|' + Style.RESET_ALL)
                    print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , Fore.RED + '|' + Style.RESET_ALL)
    
                elif dynamic_brick.strength == 0:
                    print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , ' ')
                    print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , ' ')


    def PrintClearBricks(self,fixed_bricks,dynamic_bricks):
        for fix_brick in fixed_bricks:
            print_there(fix_brick.get_xstartpos(), fix_brick.get_ystartpos() , ' ')
            print_there(fix_brick.get_xstartpos(), fix_brick.get_yendpose() , ' ')

        for dynamic_brick in dynamic_bricks:
            print_there(dynamic_brick.get_xstartpos(), dynamic_brick.get_ystartpos() , ' ')
            print_there(dynamic_brick.get_xendpose(), dynamic_brick.get_yendpose() , ' ')

    def PrintBossEnemy(self, bossenemy):
        # Take off previous position
        for i in range(bossenemy.get_xposendprev() - bossenemy.get_xposstartprev() + 1):
            for j in range(bossenemy.get_yposendprev() - bossenemy.get_yposstartprev() + 1):
                if i == 0:
                    # First layer
                    if j == 3:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j , Fore.CYAN + ' ' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j ,' ')    

                elif i == 1:
                    # second layer
                    if j == 2 or j == 3:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j , Fore.BLUE + ' ' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j ,' ')    

                elif i == 2:
                    # third layer
                    if j == 1 or j == 2 or j == 3 or j == 4:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j , Fore.WHITE + ' ' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j ,' ')    

                elif i == 3:
                    # Fourth layer
                    print_there(bossenemy.get_xposstartprev() + i, bossenemy.get_yposstartprev() + j , Fore.RED + ' ' + Style.RESET_ALL)
        #print a UFO
        for i in range(bossenemy.get_xposend() - bossenemy.get_xposstart() + 1):
            for j in range(bossenemy.get_yposend() - bossenemy.get_yposstart() + 1):
                if i == 0:
                    # First layer
                    if j == 3:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j , Fore.CYAN + '_' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j ,'|')

                elif i == 1:
                    # second layer
                    if j == 2 or j == 3:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j , Fore.BLUE + '_' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j ,'|')    

                elif i == 2:
                    # third layer
                    if j == 1 or j == 2 or j == 3 or j == 4:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j , Fore.WHITE + '_' + Style.RESET_ALL)

                    else:
                        print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j ,'|')    

                elif i == 3:
                    # Fourth layer
                    print_there(bossenemy.get_xposstart() + i, bossenemy.get_yposstart() + j , Fore.RED + '_' + Style.RESET_ALL)

    def PrintBossEnemyLife(self , health):
        health_num = int(int(health) / 10)
        for i in range(health_num + 1):
            print_there(10 , (y_screen_start + y_screen_end)/2 + i , ' ')
        for i in range(health_num):
            print_there(10 , (y_screen_start + y_screen_end)/2 + i , Fore.WHITE + '$' + Style.RESET_ALL)                        


    def PrintDropDowns(self , dropdowns):
        for dropdown in dropdowns:
            print_there(dropdown.get_xposprev() , dropdown.get_yposprev() , '    ')
            if dropdown.get_typeofpower() == 1:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.BLUE + '[+]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 2:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.RED + '[-]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 3:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.YELLOW + '[**]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 4:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.CYAN + '[+*]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 5:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.LIGHTRED_EX + '[O]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 6:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.WHITE + '[_*]' + Style.RESET_ALL)

            elif dropdown.get_typeofpower() == 7:
                print_there(dropdown.get_xpos() , dropdown.get_ypos() , Fore.LIGHTGREEN_EX + '[!!]' + Style.RESET_ALL)      

            if dropdown.get_gravity() != 0:
                dropdown.change_gravity()

    def PrintBlasters(self, blasters):
        for blaster in blasters:
            print_there(blaster.get_xpos() + 1, blaster.get_ypos() , ' ')
            print_there(blaster.get_xpos() , blaster.get_ypos() , Fore.LIGHTBLUE_EX + '|' + Style.RESET_ALL) 

    def PrintBombs(self , bombs):
        for bomb in bombs:
            print_there(bomb.get_xpos() - 1, bomb.get_ypos() , ' ')
            print_there(bomb.get_xpos() , bomb.get_ypos() , Fore.YELLOW + '!' + Style.RESET_ALL)                                                     

    def PrintRestartGameLost(self , player , ball):
        print_there((x_screen_end + x_screen_start)/2 , (y_screen_start + y_screen_end ) / 2 , Fore.MAGENTA + 'Balls Left: ' + str(ball.get_lives()) + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start)/2 + 2 , (y_screen_start + y_screen_end ) / 2 , Fore.CYAN + 'Lives Left: ' + str(player.get_lives() - 1) + Style.RESET_ALL)   

        if ball.get_lives() == 0 and player.get_lives() > 1:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Life Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)

        elif ball.get_lives() > 0:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Ball Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)

        elif player.get_lives() == 1:
            print_there((x_screen_end + x_screen_start)/2 + 4 , (y_screen_start + y_screen_end ) / 2 , Fore.YELLOW + 'Start New Game Press h' + Style.RESET_ALL)
            print_there((x_screen_end + x_screen_start)/2 + 6 , (y_screen_start + y_screen_end ) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)
    
    def PrintRestartGameWon(self , player):
        print_there((x_screen_end + x_screen_start) / 2 , (y_screen_end + y_screen_start) / 2 , Fore.BLUE + 'You Have Won !!!' + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 2 , (y_screen_end + y_screen_start) / 2 , Fore.MAGENTA + 'Score : ' + str(player.get_score()) + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 4 , (y_screen_end + y_screen_start) / 2 , Fore.WHITE + 'Time Taken : ' + str(player.get_time()) + Style.RESET_ALL)
        if player.get_level() < 3:
            print_there((x_screen_end + x_screen_start) / 2 + 6 , (y_screen_end + y_screen_start) / 2 , Fore.YELLOW + 'Start Next Level Press h' + Style.RESET_ALL)

        if player.get_level() == 3:    
            print_there((x_screen_end + x_screen_start) / 2 + 6 , (y_screen_end + y_screen_start) / 2 , Fore.YELLOW + 'Start New Game Press h' + Style.RESET_ALL)
        print_there((x_screen_end + x_screen_start) / 2 + 8 , (y_screen_end + y_screen_start) / 2 , Fore.RED + 'Quit Game Press q' + Style.RESET_ALL)