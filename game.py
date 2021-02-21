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

def Initialisation():
    
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
    for i in range(5):
        for j in range(5):
            if i == j:
                fixed_brick = Fixed_Brick(brick_x_start, brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2)
                fixed_bricks.append(fixed_brick)
    
            else:
                dynamic_brick = Dynamic_Brick(brick_x_start ,brick_y_start + 3*j , brick_x_start , brick_y_start + 3*j + 2 , random.randint(1,3) , random.randint(0,6))
                dynamic_bricks.append(dynamic_brick)

        brick_x_start = brick_x_start + 1        
    # dynamic_brick = Dynamic_Brick(brick_x_start + 2 , brick_y_start + 6, brick_x_start + 2, brick_y_start + 8 , 1 , 1)
    # dynamic_bricks.append(dynamic_brick)

    # dynamic_brick = Dynamic_Brick(brick_x_start , brick_y_start + 6, brick_x_start, brick_y_start + 8 , 3 , 1)
    # dynamic_bricks.append(dynamic_brick)  
    
    global collision
    # initialise Collision
    collision = Collision()

    global dropdowns
    dropdowns = []

    global powerup_times
    powerup_times = []

    for i in range(6):
        powerup_time = PowerupTime()
        powerup_times.append(powerup_time)

# game over
game_over = GameOver()

total_bricks_destroyed = 0
# flag for ball and board to be together
flag_together = 0 
flag_grab = 0         

update_ball_lives = 0
while 1:
    # # clear console
    # clear = lambda: os.system('clear')
    # clear()
    hide_cursor()
    if isInitialise == 0:
        Initialisation()
        if player.lives == 0:
            player.score = 0
            player.lives = 3
            player.time = 0
        player.score = 0
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

        elif char == 'q' or char == 'Q':
            Print('End')
            sys.exit(0)

        # move ball
        if flag_together == 1:
            for ball in balls:
                if ball.together == 1:
                    ball.move_ball_speed()
            player.set_run_time(int(time.time() - start_run_time))

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
                    if dynamic_brick.strength == 1 or ball.super_strength == 100:
                        total_bricks_destroyed = total_bricks_destroyed + 1
                        upd_score = dynamic_brick.strength * 10
                        if dynamic_brick.typeofdropdown != 0:
                            dropdown = DropDown(dynamic_brick.x_start_pos , dynamic_brick.y_start_pos, dynamic_brick.typeofdropdown)
                            dropdowns.append(dropdown)
                    collision.Collision_ball_dynamic_brick(ball , dynamic_brick)
    
                    player.update_score(upd_score)    
                    break

        # Dropdowns
        for dropdown in dropdowns:
            dropdown.move_dropdown()
            check_collision_with_board = collision.Collision_board_dropdown(board , dropdown)
            if check_collision_with_board == 1:
                powerup = dropdown.type_of_power
                print_there(dropdown.x_pos - 1, dropdown.y_pos , '    ')
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

                if powerup_times[powerup - 1].total_time == 0:
                    powerup_times[powerup - 1].start_time = time.time()
                    powerup_times[powerup - 1].total_time = 10

                else:
                    powerup_times[powerup - 1].total_time = powerup_times[powerup - 1].total_time  + 10          

                continue
            check_collision_with_wall = collision.Collision_dropdown_wall(board , game_screen.x_map_end)
            if check_collision_with_wall == 1:
                print_there(dropdown.x_pos , dropdown.y_pos , ' ')
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
            char = ''
            clear = lambda: os.system('clear')
            clear()
