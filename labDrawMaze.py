import pprint

width = 20
height = 10

wall = '' # символ обозначения стены
entry = '' # символ обозначения входа в лабиринт
exit = '' # символ обозначения выхода из лабиринта


def init_maze():
    maze = [0] * height
    for i in range(height):
        maze[i] = [0 for j in range(width)]
    return maze

def move(data, current_row, current_col):
    pass

def up(data):
    pass 

def right(data):
    pass 

def down(data):
    pass 

def left(data):
    pass 



maze = init_maze()
