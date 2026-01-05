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
class Ball:
    x_max = 80
    y_max = 28
    def __init__(self):
        self.x = 1
        self.y = 1
        self.speed_x = 1
        self.speed_y = 1

    def moveleft(self):
        self.x -= self.speed_x
        self.x = max(1, self.x)

    def moveright(self):
        self.x += self.speed_x
        self.x = min(self.x, Ball.x_max - 2)

    def moveup(self):
        self.y -= self.speed_y
        self.y = max(1, self.y)

    def movedown(self):
        self.y += self.speed_y
        self.y = min(self.y, Ball.y_max - 2)

class Items:
    def __init__(self, score):
        self.item_count = random.randint(3, 10)
        self.items_pos = [(random.randint(1, Ball.x_max - 2), random.randint(1, Ball.y_max - 2)) for _ in range(self.item_count)]
        self.score = score
        self.level=1
    def remove_item(self,item):
        self.items_pos.remove(item)
        self.item_count = max(0, self.item_count - 1)
        self.increase_score()
    def increase_score(self):
        self.score += 1
    def get_score(self):
        return self.score
    def get_level(self):
        return self.level
    def get_positions(self):
        return self.items_pos
    def get_item_count(self):
        return self.item_count
    def make_new_level(self):
        self.level += 1
        self.item_count = random.randint(3, 10)
        self.items_pos = [(random.randint(1, Ball.x_max - 2), random.randint(1, Ball.y_max - 2)) for _ in range(self.item_count)]

ball = Ball()
def generate_background():
    back_ground = [[' ' for _ in range(Ball.x_max)] for _ in range(Ball.y_max)]
    back_ground[0] = ['-' for _ in range(Ball.x_max)]
    back_ground[Ball.y_max-1] = ['-' for _ in range(Ball.x_max)]
    for i in range(Ball.y_max):
        back_ground[i][0] = '|'
        back_ground[i][Ball.x_max - 1] = '|'
    return back_ground

back_ground = generate_background()
items = Items(0)

def rendergrid(x_pos, y_pos):
    grid = [row[:] for row in back_ground]
    if (x_pos, y_pos) in items.get_positions():
        items.remove_item((x_pos, y_pos))

    item_count= items.get_item_count()
    items_position = items.get_positions()

    for i in range(item_count):
        grid[items_position[i][1]][items_position[i][0]] = 'X'
    grid[y_pos][x_pos] = 'O'

    print(' '*100+ f'Level:{items.get_level()}  Score:{items.get_score()*50}')
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
                ball.moveleft()
            elif key == 'd':
                ball.moveright()
            elif key == 'w':
                ball.moveup()
            elif key == 's':
                ball.movedown()
        os.system('cls')
        rendergrid(ball.x, ball.y)
        time.sleep(0.1)

# ---------- GAME START ----------
hide_cursor()
try:
    inputthread = threading.Thread(target=readinput)
    inputthread.start()
    inputthread.join()
finally:
    show_cursor()
