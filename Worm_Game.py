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
    def check_over(self,x,y,body):
        if (x,y) in body:
            self.is_over = True
        if y==0 or y==Game.y_max-1:
            self.is_over = False
        if x==0 or x==Game.x_max-1:
            self.is_over = False
    def reset_game(self):
        self.is_over=False
        self.score=0
        self.level=1
        worm.body=[]
        worm.body_size=0
        worm.last_move=0
        items.make_new_level()

game = Game(0)
class Worm:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.speed_x = 1
        self.speed_y = 1
        self.body=[]
        self.body_size = 0
        self.last_move = None
    def moveleft(self):
        self.body_pos(self.x,self.y)
        self.x -= self.speed_x
        self.x = max(1, self.x)

        self.last_move = self.moveleft

    def moveright(self):
        self.body_pos(self.x, self.y)
        self.x += self.speed_x
        self.x = min(self.x, Game.x_max - 2)

        self.last_move = self.moveright

    def moveup(self):
        self.body_pos(self.x, self.y)
        self.y -= self.speed_y
        self.y = max(1, self.y)

        self.last_move = self.moveup

    def movedown(self):
        self.body_pos(self.x, self.y)
        self.y += self.speed_y
        self.y = min(self.y, Game.y_max - 2)

        self.last_move = self.movedown

    def grow(self):
        self.body_size+=1

    def body_pos(self, x, y):
        if self.body_size> len(self.body):
            self.body.append((x,y))
        else:
            if len(self.body) > 0:
                self.body.pop(0)
                self.body.append((x,y))

    def showbody(self):
        return self.body

class Items:
    def __init__(self, score):
        self.item_count = random.randint(3, 10)
        self.items_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 2)) for _ in range(self.item_count)]
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
        self.item_count = random.randint(3, 10)
        self.items_pos = [(random.randint(1, Game.x_max - 2), random.randint(1, Game.y_max - 2)) for _ in range(self.item_count)]

worm = Worm()
def generate_background():
    back_ground = [[' ' for _ in range(Game.x_max)] for _ in range(Game.y_max)]
    back_ground[0] = ['-' for _ in range(Game.x_max)]
    back_ground[Game.y_max-1] = ['-' for _ in range(Game.x_max)]
    for i in range(Game.y_max):
        back_ground[i][0] = '|'
        back_ground[i][Game.x_max - 1] = '|'
    return back_ground

back_ground = generate_background()
items = Items(0)

def rendergrid(x_pos, y_pos):
    grid = [row[:] for row in back_ground]
    body = worm.showbody()
    game.check_over(x_pos, y_pos, body)

    if (x_pos, y_pos) in items.get_positions():
        items.remove_item((x_pos, y_pos))
        worm.grow()

    item_count= items.get_item_count()
    items_position = items.get_positions()

    for i in range(item_count):
        grid[items_position[i][1]][items_position[i][0]] = 'X'
    grid[y_pos][x_pos] = 'O'

    for u,v in body:
        grid[v][u] = 'o'

    print(' '*100+ f'Level:{game.get_level()}  Score:{game.get_score()*50}')
    for row in grid:
        print(''.join(row))
    if items.get_item_count() == 0:
        items.make_new_level()

def readinput():
    print("WASD to move, Q to quit")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8', errors='ignore')

            if key == 'q':
                break
            elif key == 'a':
                worm.moveleft()
            elif key == 'd':
                worm.moveright()
            elif key == 'w':
                worm.moveup()
            elif key == 's':
                worm.movedown()
            elif key == 'r':
                game.reset_game()
        else:
            if worm.last_move:
                worm.last_move()
        if game.get_status():
            break
        os.system('cls')
        rendergrid(worm.x, worm.y)
        time.sleep(0.1)

# ---------- GAME START ----------
hide_cursor()
try:
    inputthread = threading.Thread(target=readinput)
    inputthread.start()
    inputthread.join()
finally:
    show_cursor()
