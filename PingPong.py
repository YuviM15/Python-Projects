import threading
import time
import msvcrt
import os
import ctypes
import random
# ---------- CURSOR CONTROL ----------
class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),
                ("visible", ctypes.c_bool)]

def hide_cursor():
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    cursor = CONSOLE_CURSOR_INFO(1, False)
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor))

def show_cursor():
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    cursor = CONSOLE_CURSOR_INFO(1, True)
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor))
# -----------------------------------
class Game:
    x_max = 80
    x_min = 0
    y_max = 28
    def __init__(self,score):
        self.is_over=False
        self.score = score
        self.level=1
    def increase_score(self):
        self.score += 1
    def get_score(self):
        return self.score
    def get_level(self):
        return self.level
    def get_status(self):
        return self.is_over
    def check_over(self,x,y,stick):
        if (y,x) in stick:
            self.is_over = False
        elif y==Game.y_max-1:
            self.is_over = True
    def reset_game(self):
        self.is_over=False
        self.score=0
        items.make_new_level()
        powerup_double.make_new_level()
        powerup_extend.make_new_level()
        racket.restore()
        self.level=1

game = Game(0)
class Racket:
    def __init__(self):
        self.length=10
        self.original_length= self.length
        self.x1 = Game.x_min+1
        self.x2 = self.x1 + self.length
        self.y = Game.y_max-2
        self.speed_x = 2
        self.divider=self.length//10
    def inc_length(self):
        self.length+=5
        self.x2 = self.x1+ self.length
    def restore(self):
        self.length=self.original_length
    def moveleft(self):
        self.x1 -= self.speed_x
        self.x2 = self.x1 + self.length
        self.x1 = max(Game.x_min+1, self.x1)
        self.x2 = max(Game.x_min+1+self.length, self.x2)

    def moveright(self):
        self.x1 += self.speed_x
        self.x2 = self.x1+ self.length
        self.x1 = min(Game.x_max-2-self.length, self.x1)
        self.x2 = min(Game.x_max-2, self.x2)
    def position(self):
        self.x2= min(self.x2,game.x_max-1)
        self.x1 = max(self.x1,Game.x_min+1)
        return [(self.y,l) for l in range(self.x1,self.x2)]
    def midpoint(self):
        return (self.y,(self.x1+self.x2)//2)

    def getmidsection(self):
        return [(self.y,l) for l in range(self.midpoint()[1]-self.divider,self.midpoint()[1]+self.divider)]
    def getleftsection(self):
        return [(self.y,l) for l in range(self.x1,self.midpoint()[1]-self.divider)]
    def getrightsection(self):
        return [(self.y,l) for l in range(self.midpoint()[1]+self.divider,self.x2)]
racket= Racket()

class Ball:
    number_of_balls=1
    def __init__(self):
        self.y , self.x = racket.midpoint()
        self.speed_x = 1
        self.speed_y = -1
    def set_position(self,a,b):
        self.x = a
        self.y = b
    def set_speed_x(self,vel_x):
        self.speed_x = vel_x
    def sidewalls(self):
        self.speed_x = -1*self.speed_x

    def topwall(self):
        self.speed_y = -1*self.speed_y


    def hitmid(self):
        self.speed_y = -1
        self.speed_x = 0
    def hitleft(self):
        self.speed_y = -1
        if self.speed_x==0:
            self.speed_x = -1
    def hitright(self):
        self.speed_y = -1
        if self.speed_x==0:
            self.speed_x = 1


    def move(self):
        self.y += self.speed_y
        self.x += self.speed_x


class Items:
    def __init__(self):
        self.item_count = random.randint(15, 40)
        self.items_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 10)) for _ in range(self.item_count)]
    def remove_item(self,item):
        self.items_pos.remove(item)
        self.item_count = max(0, self.item_count - 1)
        game.increase_score()
    def get_positions(self):
        return self.items_pos
    def get_item_count(self):
        return self.item_count
    def make_new_level(self):
        game.level += 1
        self.item_count = random.randint(15, 40)
        self.items_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 10)) for _ in range(self.item_count)]

class Powerup:
    def __init__(self):
        self.powerup_count = random.randint(20, 50)
        self.powerup_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 10)) for _ in range(self.powerup_count)]
        self.falling = []
    def remove_powerup(self,item):
        self.powerup_pos.remove(item)
        self.powerup_count = max(0, self.powerup_count - 1)
        game.increase_score()
    def get_powerup_positions(self):
        return self.powerup_pos
    def get_powerup_count(self):
        return self.powerup_count
    def set_falling(self,x,y):
        self.falling.append((x,y))
    def falling_powerup(self):
        for x, y in self.falling[:]:
            if y==Game.y_max-1:
                self.falling.remove((x,y))
            else:
                self.falling.remove((x,y))
                self.falling.append((x,y+1))
    def get_fallinglist(self):
        return self.falling
    def activate_powerup(self):
        racket.inc_length()
    def make_new_level(self):
        self.powerup_count = random.randint(20, 50)
        self.powerup_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 10)) for _ in range(self.powerup_count)]

balls_list = [Ball()]
def generate_background():
    back_ground = [[' ' for _ in range(Game.x_max)] for _ in range(Game.y_max)]
    back_ground[0] = ['-' for _ in range(Game.x_max)]
    back_ground[Game.y_max-1] = ['-' for _ in range(Game.x_max)]
    for i in range(Game.y_max):
        back_ground[i][0] = '|'
        back_ground[i][Game.x_max - 1] = '|'
    return back_ground

back_ground = generate_background()
items = Items()
powerup_double = Powerup()
powerup_extend=Powerup()
def rendergrid():
    grid = [row[:] for row in back_ground]
    stick= racket.position()

    ###Render Items
    item_count= items.get_item_count()
    items_position = items.get_positions()
    for i in range(item_count):
        grid[items_position[i][1]][items_position[i][0]] = '*'  ####Item

    ###Render Double Powerups
    powerup_count= powerup_double.get_powerup_count()
    powerup_position = powerup_double.get_powerup_positions()
    for i in range(powerup_count):
        grid[powerup_position[i][1]][powerup_position[i][0]] = '#' ####Powerup
    falling_powerup = powerup_double.get_fallinglist()
    for x,y in falling_powerup:
        grid[y][x] = '#'
        if (y,x) in stick:
            new_list=[]
            for b in balls_list:
                new_ball = Ball()
                new_ball.set_position(b.x, b.y)
                new_list.append(new_ball)
            balls_list.extend(new_list)
            Ball.number_of_balls+=len(new_list)

    #####Extend Powerup
    powerup_count_extend= powerup_extend.get_powerup_count()
    powerup_position_extend = powerup_extend.get_powerup_positions()
    for i in range(powerup_count_extend):
        grid[powerup_position_extend[i][1]][powerup_position_extend[i][0]] = '-' ####Powerup
    falling_powerup_extend = powerup_extend.get_fallinglist()
    for x,y in falling_powerup_extend:
        grid[y][x] = '@'
        if (y,x) in stick:
            racket.inc_length()
            powerup_extend.falling.remove((x, y))
            # powerup.activate_powerup()
            # stick = racket.position()

    for u,v in stick:
        grid[u][v] = '_'   ###Stick
    for ball in balls_list:
        renderball(ball)
        if 0 <= ball.y < Game.y_max and 0 <= ball.x < Game.x_max:
            grid[ball.y][ball.x] = 'o'

    ###Score Card
    print(' '*100+ f'Level:{game.get_level()}  Score:{game.get_score()*50}')
    for row in grid:
        print(''.join(row))
    if items.get_item_count() == 0:
        items.make_new_level()



def renderball(ball):
    x_pos, y_pos = ball.x, ball.y
    if ball.y >= Game.y_max - 1:
        if Ball.number_of_balls == 1:
            game.is_over = True
        else:
            balls_list.remove(ball)
            Ball.number_of_balls -= 1
        return
    if (x_pos, y_pos) in items.get_positions():
        items.remove_item((x_pos, y_pos))
        # ball.topwall()
    ###Falling Powerups
    if (x_pos, y_pos) in powerup_double.get_powerup_positions():
        powerup_double.remove_powerup((x_pos, y_pos))
        powerup_double.set_falling(x_pos, y_pos)
    powerup_double.falling_powerup()

    if (x_pos, y_pos) in powerup_extend.get_powerup_positions():
        powerup_extend.remove_powerup((x_pos, y_pos))
        powerup_extend.set_falling(x_pos, y_pos)
    powerup_extend.falling_powerup()

    if y_pos==0:
        ball.topwall()
    elif (y_pos, x_pos) in racket.getmidsection():
        ball.hitmid()
    elif (y_pos, x_pos) in racket.getleftsection():
        ball.hitleft()
    elif (y_pos, x_pos) in racket.getrightsection():
        ball.hitright()
    elif x_pos == 0 or x_pos == Game.x_max-1:
        ball.sidewalls()

def readinput():
    print("WASD to move, Q to quit")
    frame_rate=15   ####fps
    pause=False
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8', errors='ignore')

            if key == 'q':
                break
            elif key == 'a':
                racket.moveleft()
            elif key == 'd':
                racket.moveright()
            elif key == 'r':
                game.reset_game()
            elif key == 'p':
                pause=pause^1
        if game.get_status():
            break
        os.system('cls')
        if not pause:
            for ball in balls_list:
                ball.move()
        rendergrid()
        time.sleep(1/frame_rate)

# ---------- GAME START ----------
hide_cursor()
try:
    inputthread = threading.Thread(target=readinput)
    inputthread.start()
    inputthread.join()
finally:
    show_cursor()
