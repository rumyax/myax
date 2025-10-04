import os
from math import trunc
from random import random
from time import sleep

digit = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
signs = '`-=~!@#$%^&*()_+[]\\{}|;\':",./<>?'

matrix = digit + alpha + signs
length = len(matrix)

width, height, area, rain, fall = 0, 0, 0, '', []

while True:
    try:
        size = os.get_terminal_size()
        if width != size.columns or height != size.lines:
            [width, height] = [size.columns, size.lines]
            area = width * height
            rain = area * ' '
            fall = width * [False]
            edge = width - 1

        line = ''
        for i in range(width):
            fall[i] = random() > 0.1 if fall[i] else random() < 0.01

            if i == edge:
                line += '\n'
            elif i > 0 and fall[i]:
                line += matrix[trunc(length * random())]
            else:
                line += ' '

        rain = (line + rain)[:area]
        print(rain, end='\r')
        sleep(0.1)
    except KeyboardInterrupt:
        break

os.system('cls' if os.name == 'nt' else 'clear')
print('\n  Wake up, the Matrix has you...', end='\n\n')
