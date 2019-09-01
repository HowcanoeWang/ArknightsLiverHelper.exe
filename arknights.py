import os
import time
import pyautogui as pag
from random import randrange   # (start, stop, step)

st_btn = [2063, 1269]
operation_btn = [2007, 1091]
confirm_btn = [1475, 866]
    
def click_position(pos, range=20):
    x, y = pos
    rand_x = randrange(-range*2, range*2, 1)
    rand_y = randrange(-range, range, 1)
    pag.moveTo(x+rand_x, y+rand_y)
    print(f'Click({x+rand_x}, {y+rand_y})')
    time.sleep(3)
    pag.click()
    
def of_7(working_time):
    print('[OF-7]========Start========')
    time.sleep(3)
    click_position(st_btn)
    time.sleep(3)
    print('[OF-7] sleep 2s')
    click_position(operation_btn)
    print('[OF-7] Operating')
    time.sleep(working_time)
    click_position(confirm_btn, 100)
    print('[OF-7] Finish')
    
    
if __name__ == '__main__':
    mode = input('[Sys] Please Choose mode: [Get], [of_7], [of_f4]\n')
    if mode == 'Get':
        while True:
            x,y = pag.position()
            time.sleep(1)
            print(f'{x}, {y}')
    elif mode == 'of_7':
        loops = input('[Sys] How many times?:')
        for i in range(int(loops)):
            of_7(2*60+20)
            print(f'[Sys]Loop {i + 1} finished')
    elif mode == 'of_f4':
        loops = input('[Sys] How many times?:')
        for i in range(int(loops)):
            of_7(2*60+10)
            print(f'[Sys]Loop {i + 1} finished')