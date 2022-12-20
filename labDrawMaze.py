import pprint
import random
import time 


width = 20
height = 10

height = height - 1 if height % 2 == 0 else height
width = width - 1 if width % 2 == 0 else width

wall = '█' # символ обозначения стены
up_entry = '▼' 
right_entry = '◄'
down_entry = '▲'
left_entry = '►' # символ обозначения входа в лабиринт
exit = '▒' # символ обозначения выхода из лабиринта

maze_info = {'start_sym': up_entry, 'entry_pos': (0, 0),'exit_pos': (0, 0), 'rows': height, 'cols': width}

def init_maze():
    maze = [0] * height
    for i in range(height):
        maze[i] = [0 for j in range(width)]
    return maze

def is_finish(data, current_row, current_col):
    rows = len(data)
    cols = len(data[0])
    if current_row + 1 >= rows or current_row - 1 <= 0:
        return True
    
    if current_col + 1 >= cols or current_col - 1 <= 0:
        return True
    
    return False

def up(data,current_row, current_col):
    new_row = current_row - 1
    new_col = current_col
    data[new_row][new_col] = 2
    return (new_row, new_col)

def right(data, current_row, current_col):
    new_row = current_row
    new_col = current_col + 1
    data[new_row][new_col] = 2
    return (new_row, new_col) 

def down(data, current_row, current_col):
    new_row = current_row + 1
    new_col = current_col
    data[new_row][new_col] = 2
    return (new_row, new_col) 

def left(data, current_row, current_col):
    new_row = current_row
    new_col = current_col - 1
    data[new_row][new_col] = 2
    return (new_row, new_col)

previous_coords = []

def check_move(current_row, current_col):
    rows = maze_info['rows']
    cols = maze_info['cols']
    
    if current_row - 1 <= 0 or current_row + 1 >= rows:
        return False
    
    if current_col - 1 <= 0 or current_col + 1 >= cols:
        return False
    
    if (current_row, current_col) in previous_coords:
        return False
    
    return True
    

def move(data, current_row, current_col):
    directions = [up,right,down,left]
    direction = random.choice(directions)
    previous_coords.append((current_row, current_col))
    current_row, current_col = direction(data, current_row, current_col)
    
    if check_move(current_row, current_col):
        dig(data,current_row, current_col)
        return current_row, current_col
    
    return previous_coords[-1]
            

def init_start(data,rows,cols):
    position = random.randint(1,4)
    current_row = 0
    current_col = 0
    if position == 1: # up
        current_col = random.randint(1,cols - 1)
        maze_info['start_sym'] = up_entry
    elif position == 2: # right
        current_row = random.randint(1,rows - 1)
        current_col = cols - 1
        maze_info['start_sym'] = right_entry
    elif position == 3: # down
        current_row = rows - 1
        current_col = random.randint(1,cols - 1)
        maze_info['start_sym'] = down_entry
    elif position == 4: # left
        current_row = random.randint(1,rows - 1)
        maze_info['start_sym'] = left_entry
    
    maze_info['entry_pos'] = (current_row, current_col)
    data[current_row][current_col] = 1
    return (current_row, current_col)


def additional_dig(data, current_row, current_col):
    directions = [up,right,down,left]
    current_row, current_col = random.choice(directions)(data, current_row, current_col)
    print_maze(data)
    time.sleep(1)
    
    while True:
        if is_finish(data, current_row + 1, current_col + 1) or is_finish(data, current_row - 1, current_col - 1):
            break
        dig(data,current_row, current_col)
    
    

def dig(data, current_row, current_col):
    print_maze(data)
    time.sleep(0.5)
    number = random.randint(0,1)
    if number == 1:
        additional_dig(data, current_row, current_col)
    
    while True:
        if is_finish(data, current_row, current_col):
            break
        
    
    if is_finish(data, current_row, current_col):
        return False
    
        
def start_game():
    maze = init_maze()
    current_row, current_col = init_start(maze, height, width)
    generate = True 
    while generate:
        dig(maze, current_row, current_col)
    

def print_maze(maze):
    printable_maze = ''
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 0:
                printable_maze += wall 
            elif maze[i][j] == 1:
                printable_maze += maze_info['start_sym']
            elif maze[i][j] == 2:
                printable_maze += ' '
            elif maze[i][j] == 3:
                printable_maze += exit
        printable_maze += '\n'
    print(printable_maze)

maze = start_game()
print_maze(maze)
