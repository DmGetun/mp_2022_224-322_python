from random import randint
from pprint import pprint
import copy
import numpy as np

def reflect_left(matrix):
    result = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            result[i][j] = matrix[i][len(matrix[i]) - j - 1]
    return result

def reflect_right(matrix):
    return reflect_left(matrix)

def reflect_up(matrix):
    result = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        result[i] = matrix[len(matrix) - i - 1]
    return result

def reflect_down(matrix):
    return reflect_up(matrix)

def transpose(matrix):
    tran_matrix = [0] * len(matrix[0])
    for i in range(len(matrix[0])):
        tran_matrix[i] = [0] * len(matrix)
        
    for i in range(len(matrix[0])):
        for j in range(len(matrix)):
            tran_matrix[i][j] = matrix[j][i]
    return tran_matrix

def step_left(matrix):
    matr = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            matr[i][j] = matrix[i][j + 1]

    for i in range(len(matrix)):
        matr[i][len(matr[0]) - 1] = matrix[i][0]
    
    return matr

def step_right(matrix):
    matr = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1):
            matr[i][j + 1] = matrix[i][j]

    for i in range(len(matrix)):
        matr[i][0] = matrix[i][len(matr[0]) - 1]
    
    return matr

def rotate_left(matrix):
    return reflect_up(transpose(matrix))

def rotate_right(matrix):
    return reflect_right(transpose(matrix))



height = 4
width = 5


matrix = [0] * height
for i in range(height):
    matrix[i] = [0] * width
    
for i in range(height):
    for j in range(width):
        matrix[i][j] = randint(10,99)
    
while True:
    print(f'Матрица[{height}][{width}]:')
    pprint(matrix)
    text = '''
Выберите действие:
    1) Отразить матрицу по горизонтали
    2) Отразить матрицу по вертикали
    3) Сдвинуть матрицу на 1 шаг влево
    4) Сдвинуть матрицу на 1 шаг вправо
    5) Транспонировать матрицу
    6) Повернуть матрицу на 90 градусов влево
    7) Повернуть матрицу на 90 градусов вправо
    8) Завершить программу\n
    '''
    action_id = int(input(text + 'Ваш выбор:'))
    if action_id == 8:
        break
    actions = [reflect_left,reflect_up,step_left,step_right,transpose,rotate_left,rotate_right]
    matrix = actions[action_id - 1](matrix)
    pprint(matrix)