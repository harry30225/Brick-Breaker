import os
import sys
import random
import signal
import time
from config import *
from objects import *
from game_screen import *
from getinput import *
from AlarmException import *
from collisions import *
from gameover import *
from dropdown import *
from powerup_time import *
from blaster import *
from colorama import Fore, Back , Style


# Print at desired position
def print_there(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text))
     sys.stdout.flush()

# clear console
clear = lambda: os.system('clear')
clear()

# Hide Cursor
if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

# Take Input
getch = GetInput()

def alarmHandler(signum, frame):
    raise AlarmException

def take_input(timeout=1):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL,0.1)
    try:
        text = getch()
        signal.alarm(0)
        signal.setitimer(signal.ITIMER_REAL,0)
        return text
    except AlarmException:
        text = "n"
    signal.setitimer(signal.ITIMER_REAL,0)
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return 'n'

#initialise game map
game_screen = Game_Screen()

# initalise user
player = User()

def newPlayer():
    player = User()

isInitialise = 0
isGameLost = 0
isGameWon = 0

def Initialisation(level):
    
    global balls
    # initalise ball
    balls = []
    ball = Ball()
    balls.append(ball)
    
    global board
    #initalise board
    board = Board()
    
    global fixed_bricks
    global dynamic_bricks
    #initialise Brickset
    fixed_bricks = []
    dynamic_bricks = []
    
    brick_x_start = (x_screen_end + x_screen_start)/2 - 2
    brick_y_start = (y_screen_end + y_screen_start)/2 - 8
    #the fixed or unbreakable bricks and dynamic break
    # if level == 1:
    #     for i in range(5):
    #         for j in range(5):
    #             if i == j:
    #                 fixed_brick = Fixed_Brick(brick_x_start, brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2)
    #                 fixed_bricks.append(fixed_brick)
        
    #             else:
    #                 dynamic_brick = Dynamic_Brick(brick_x_start ,brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2 , random.randint(1,3) , random.randint(0,6), random.randint(0,1))
    #                 dynamic_bricks.append(dynamic_brick)
    
    #         brick_x_start = brick_x_start + 1
    
    # brick_x_start = (x_screen_end + x_screen_start)/2 - 2
    # brick_y_start = (y_screen_end + y_screen_start)/2 - 8

    # if level == 2 or level == 3:
    #     for i in range(5):
    #         for j in range(5):
    #             if (4 - i) == j:
    #                 fixed_brick = Fixed_Brick(brick_x_start, brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2)
    #                 fixed_bricks.append(fixed_brick)
        
    #             else:
    #                 dynamic_brick = Dynamic_Brick(brick_x_start ,brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2 , random.randint(1,3) , random.randint(0,7), random.randint(0,1))
    #                 dynamic_bricks.append(dynamic_brick)
    
    #         brick_x_start = brick_x_start + 1

    dynamic_brick = Dynamic_Brick(brick_x_start + 2 , brick_y_start + 6, brick_x_start + 2, brick_y_start + 8 , 1 , 7,0)
    dynamic_bricks.append(dynamic_brick)

    dynamic_brick = Dynamic_Brick(brick_x_start , brick_y_start + 5, brick_x_start, brick_y_start + 7 , 3 , 1,1)
    dynamic_bricks.append(dynamic_brick)

    dynamic_brick = Dynamic_Brick(brick_x_start , brick_y_start + 9, brick_x_start, brick_y_start + 11 , 3 , 1,0)
    dynamic_bricks.append(dynamic_brick)  
    
    global collision
    # initialise Collision
    collision = Collision()

    global dropdowns
    dropdowns = []

    global blasters
    blasters = []

    global powerup_times
    powerup_times = []

    for i in range(7):
        powerup_time = PowerupTime()
        powerup_times.append(powerup_time)

# game over
game_over = GameOver()

total_bricks_destroyed = 0
# flag for ball and board to be together
flag_together = 0 
flag_grab = 0
last_launch = 0         

update_ball_lives = 0
while 1:
    # # clear console
    # clear = lambda: os.system('clear')
    # clear()
    hide_cursor()
    if isInitialise == 0:
        Initialisation(player.level)
        if player.lives == 0:
            player.reset_attri()
        player.time = 0
        for ball in balls:
            ball.update_live(update_ball_lives)
        isInitialise = 1
        total_bricks_destroyed = 0

    if isGameLost == 0 and isGameWon == 0:
        # Print Game
        game_screen.PrintHeader(player)
        game_screen.PrintBoundary()
        for ball in balls:
            game_screen.PrintBall(ball)
        game_screen.PrintBoard(board)
        game_screen.PrintBricks(fixed_bricks , dynamic_bricks)
        game_screen.PrintDropDowns(dropdowns)
        game_screen.PrintBlasters(blasters)

        # taking input
        char = ''
        char = take_input()
        print("\x1B[F\x1B[2K", end="")
        if char == 'a' or char == 'A':
            for ball in balls:
                if flag_together == 0 or ball.together == 0:
                    ball.move_ball(-1)
                
            board.move_board(-1)
            char = ''

        elif char == 'd' or char == 'D':
            for ball in balls:
                if flag_together == 0 or ball.together == 0:
                    ball.move_ball(1)
                
            board.move_board(1)
            char = ''

        elif ( char == 'b' or char == 'B' ) and (flag_together == 0 or ball.together == 0):
            for ball in balls:
                if flag_together == 0 or ball.together == 0:
                    if flag_together == 0:
                        flag_together = 1
                        ball.change_together_status(1)
                        ball.set_initial_speed()
                        board.inc_speed_board(5*board.speed)
                        start_run_time = time.time()
        
                    else:
                        ball.change_together_status(1)
                        board.inc_speed_board(5)    
            char = ''

        elif char == 's' or char == 'S':
            isGameWon = 1    

        elif char == 'q' or char == 'Q':
            Print('End')
            sys.exit(0)

        # move ball
        if flag_together == 1:
            for ball in balls:
                if ball.together == 1:
                    ball.move_ball_speed()
            player.set_run_time(int(time.time() - start_run_time))

        # shooting blasters
        # making blasters
        if board.activate_shoot == 1 and int(time.time() - last_launch) == 1:
            last_launch = int(time.time())
            new_blaster_1 = Blaster(board.x_pos - 1 , board.y_pos + (board.length - 1 - (board.length/2)))
            new_blaster_2 = Blaster(board.x_pos - 1 , board.y_pos + (0 - (board.length/2)))
            blasters.append(new_blaster_1)
            blasters.append(new_blaster_2)
        # move blaster
        for blaster in blasters:
            blaster.move_blaster()

        # show time
        if board.activate_shoot == 1:
            print_there(10 , (y_screen_end + y_screen_start)/2 , 'Blaster Time : ' + str(int(time.time() - powerup_times[6].start_time)))        


        for ball in balls:
            # Collisions
            # Collision with Wall
            if (ball.x_pos_prev >= game_screen.x_map_begin) and (ball.x_pos <= game_screen.x_map_begin):
                collision.Collision_ball_wall(ball , game_screen)
    
            if ((ball.y_pos_prev >= game_screen.y_map_begin) and (ball.y_pos <= game_screen.y_map_begin)) or ((ball.y_pos_prev <= game_screen.y_map_end) and (ball.y_pos >= game_screen.y_map_end)):
                collision.Collision_ball_wall(ball , game_screen)    

            # Collision with Board
            if (ball.x_pos == board.x_pos) and ball.together == 1:
                collision_board = collision.Collision_ball_board(ball , board)
                if collision_board == 1 and flag_grab == 1:
                    ball.change_together_status(0)
                    board.inc_speed_board(1)
                    ball.x_pos = ball.x_pos - 1

                # falling bricks
                if collision_board == 1 and int(time.time() - start_run_time) > 5:
                    game_screen.PrintClearBricks(fixed_bricks,dynamic_bricks)
                    for fixed_brick in fixed_bricks:
                        fixed_brick.dec_pos()
                        if fixed_brick.x_start_pos >= board.x_pos:
                            isGameLost = 1
                            player.lost_lives()
                            break
                    
                    for dynamic_brick in dynamic_bricks:
                        dynamic_brick.dec_pos()
                        if dynamic_brick.x_start_pos >= board.x_pos:
                            isGameLost = 1
                            player.lost_lives()
                            break        

            # Collision with Fixed Bricks
            for fixed_brick in fixed_bricks:
                if ball.x_pos == fixed_brick.x_start_pos and ball.y_pos >= fixed_brick.y_start_pos and ball.y_pos <= fixed_brick.y_end_pos:
                    collision.Collision_ball_fixed_brick(ball , fixed_brick)
                    if ball.super_strength == 100:
                        player.update_score(40)
                    break

            # Collision with Dynamic Bricks
            for dynamic_brick in dynamic_bricks:
                if ball.x_pos == dynamic_brick.x_start_pos and ball.y_pos >= dynamic_brick.y_start_pos and ball.y_pos <= dynamic_brick.y_end_pos and dynamic_brick.strength > 0:
                    upd_score = 10
                    dynamic_brick.change_rainbow()
                    if dynamic_brick.strength == 1 or ball.super_strength == 100:
                        total_bricks_destroyed = total_bricks_destroyed + 1
                        upd_score = dynamic_brick.strength * 10
                        if dynamic_brick.typeofdropdown != 0:
                            dropdown = DropDown(dynamic_brick.x_start_pos , dynamic_brick.y_start_pos, dynamic_brick.typeofdropdown,ball.x_speed,ball.y_speed , -4)
                            dropdowns.append(dropdown)
                    collision.Collision_ball_dynamic_brick(ball , dynamic_brick)
    
                    player.update_score(upd_score)    
                    break

        # Blasters
        for blaster in blasters:
            # Collision with Fixed Bricks
            for fixed_brick in fixed_bricks:
                if ball.x_pos == fixed_brick.x_start_pos and ball.y_pos >= fixed_brick.y_start_pos and ball.y_pos <= fixed_brick.y_end_pos:
                    print_there(blaster.x_pos , blaster.y_pos , ' ')
                    print_there(blaster.x_pos + 1, blaster.y_pos , ' ')
                    blasters.remove(blaster)
                    break

            # collision with dynamic bricks
            for dynamic_brick in dynamic_bricks:
                if blaster.x_pos <= dynamic_brick.x_start_pos and blaster.y_pos >= dynamic_brick.y_start_pos and blaster.y_pos <= dynamic_brick.y_end_pos and dynamic_brick.strength > 0:
                    upd_score = 10
                    dynamic_brick.change_rainbow()
                    if dynamic_brick.strength == 1:
                        total_bricks_destroyed = total_bricks_destroyed + 1
                        if dynamic_brick.typeofdropdown != 0:
                            dropdown = DropDown(dynamic_brick.x_start_pos , dynamic_brick.y_start_pos, dynamic_brick.typeofdropdown,1,0 , 0)
                            dropdowns.append(dropdown)
                    dynamic_brick.dec_str(0)
                    player.update_score(upd_score)
                    print_there(blaster.x_pos , blaster.y_pos , ' ')
                    print_there(blaster.x_pos + 1, blaster.y_pos , ' ')
                    blasters.remove(blaster)
                    break        

            # collision with upper roof
            if blaster.x_pos <= game_screen.x_map_begin:
                print_there(blaster.x_pos , blaster.y_pos , ' ')
                print_there(blaster.x_pos + 1, blaster.y_pos , ' ')
                blasters.remove(blaster)        

        # Dropdowns
        for dropdown in dropdowns:
            dropdown.move_dropdown()
            check_collision_with_board = collision.Collision_board_dropdown(board , dropdown)
            # collision.Collision_dropdown_sidewalls(dropdown , game_screen.x_map_begin , game_screen.y_map_begin , game_screen.y_map_end)
            if check_collision_with_board == 1:
                powerup = dropdown.type_of_power
                print_there(dropdown.x_pos_prev , dropdown.y_pos_prev , '    ')
                print_there(dropdown.x_pos , dropdown.y_pos , '    ')
                dropdowns.remove(dropdown)
                if powerup == 1:
                    board.inc_length_board()

                elif powerup == 2:
                    for i in range(board.length):
                        print_there(board.x_pos , board.y_pos + ( i - (board.length / 2)), ' ')
                    board.dec_length_board()

                elif powerup == 3:
                    balls_new = []
                    for ball in balls:
                        ballnew = Ball()
                        ballnew.update_config(ball)
                        balls_new.append(ballnew)

                    for ballnew in balls_new:
                        balls.append(ballnew)    

                elif powerup == 4:
                    for ball in balls:
                        ball.inc_speed_ball()

                elif powerup == 5:
                    for ball in balls:
                        ball.update_super_strength(100)

                elif powerup == 6:
                    flag_grab = 1
                    board.inc_speed_board(1)

                elif powerup == 7:
                    # Shooting paddles
                    board.activate_blasters()

                if powerup_times[powerup - 1].total_time == 0:
                    powerup_times[powerup - 1].start_time = time.time()
                    if powerup == 7:
                        last_launch = int(powerup_times[6].start_time)
                    powerup_times[powerup - 1].total_time = 10

                else:
                    powerup_times[powerup - 1].total_time = powerup_times[powerup - 1].total_time  + 10          

                continue
            check_collision_with_wall = collision.Collision_dropdown_wall(dropdown , game_screen.x_map_end)
            if check_collision_with_wall == 1:
                # dropdown.x_speed = -1 * dropdown.x_speed
                print_there(dropdown.x_pos , dropdown.y_pos , '     ')
                print_there(dropdown.x_pos_prev , dropdown.y_pos_prev , '    ')
                print_there(dropdown.x_pos + dropdown.x_speed, dropdown.y_pos + dropdown.y_speed , '    ')
                dropdowns.remove(dropdown)

        for i in range(len(powerup_times)):
            if i != 2:
                if time.time() - powerup_times[i].start_time >= powerup_times[i].total_time and powerup_times[i].total_time > 0:
                    powerup_times[i].total_time = 0
                    powerup_times[i].start_time = 0
                    if i == 0:
                        for i in range(board.length):
                            print_there(board.x_pos , board.y_pos + ( i - (board.length / 2)), ' ')
                        board.dec_length_board()

                    elif i == 1:
                        board.inc_length_board()

                    elif i == 3:
                        for ball in balls:
                            ball.dec_speed_ball()

                    elif i == 4:
                        for ball in balls:
                            ball.update_super_strength(0)

                    elif i == 5:
                        flag_grab = 0
                        board.inc_speed_board(5)

                    elif i == 6:
                        # disable shooting
                        board.deactivate_blasters()
                        print_there(10 , (y_screen_end + y_screen_start)/2 , '                   ')
                        print_there(board.x_pos_prev - 1 , board.y_pos_prev + (0 - (board.length/2)) , ' ')
                        print_there(board.x_pos_prev - 1 , board.y_pos_prev + (board.length_prev - 1 - (board.length/2)) , ' ')
                        print_there(board.x_pos - 1 , board.y_pos + (0 - (board.length/2)) , ' ')
                        print_there(board.x_pos - 1 , board.y_pos + (board.length - 1 - (board.length/2)) , ' ')                                

        # Game Over
        for ball in balls:
            gamelost = game_over.gameLost(ball , game_screen)
            if gamelost == 1 and len(balls) > 1:
                print_there(ball.x_pos_prev , ball.y_pos_prev , ' ')
                balls.remove(ball)
                gamelost = 0

            elif gamelost == 1 and len(balls) == 1:
                isGameLost = 1
                end_run_time = time.time()
                player.set_run_time(int(end_run_time - start_run_time))
                gamelost = 0

        gamewon = game_over.gameWon(total_bricks_destroyed , len(dynamic_bricks))
        if gamewon == 1:
            isGameWon = 1
            end_run_time = time.time()
            player.set_run_time(int(end_run_time - start_run_time))    

    elif isGameLost == 1:
        clear = lambda: os.system('clear')
        clear()
        game_screen.PrintHeader(player)
        for ball in balls:
            game_screen.PrintRestartGameLost(player , ball)
        # taking input
        char = take_input()
        print("\x1B[F\x1B[2K", end="")
        # print(char)
        if char == 'q' or char == 'Q':
            print('End')
            sys.exit(0)

        elif char == 'h' or char =='H':
            isGameLost = 0
            isGameWon = 0
            isInitialise = 0
            flag_together = 0
            flag_grab = 0
            player.reset_score()
            for ball in balls:
                update_ball_lives = ball.lives
                if ball.lives == 0 and player.lives > 0:
                    player.dec_live_user() 
            char = ''
            clear = lambda: os.system('clear')
            clear()   

    elif isGameWon == 1:
        clear = lambda: os.system('clear')
        clear()
        game_screen.PrintHeader(player)
        game_screen.PrintRestartGameWon(player)
         # taking input
        char = take_input()
        print("\x1B[F\x1B[2K", end="")
        # print(char)
        if char == 'q' or char == 'Q':
            print('End')
            sys.exit(0)

        elif char == 'h' or char =='H':
            isGameWon = 0
            isGameLost = 0
            isInitialise = 0
            flag_together = 0
            flag_grab = 0
            if player.level < 3:
                player.inc_level()

            else:
                player.level = 1    
            char = ''
            clear = lambda: os.system('clear')
            clear()
