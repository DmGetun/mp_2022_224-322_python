import random

symbol = '██'
space = '  '
block = '░░'

height = int(input('Введите высоту поля: '))
width = int(input('Введите ширину поля: '))

height = height - 1 if height % 2 == 0 else height
width = width - 1 if width % 2 == 0 else width


print(symbol * width)

for i in range(height):
    line = symbol
    for j in range(width - 2):
        fill_char = space if random.randint(0,1) else block
        if i % 2 != 0:
            if j % 2 == 0:
                line += fill_char
            else:
                line += symbol
        else:
            line += fill_char
    print(line + symbol)

print(symbol * width)