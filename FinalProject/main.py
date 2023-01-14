import argparse
from db import DataBase

parser = argparse.ArgumentParser(
    prog="Финальный проект по курсу программированию на python",
    description='Программа предназначена для синхронизации папок',
    epilog="(c) Гетун Дмитрий, группа 224-322"
)

parser.add_argument('-s', '--source', nargs='+', default='') # путь к папке-источнику
parser.add_argument('-d', '--destination', nargs='+', default='') # путь к папке-назначения
parser.add_argument('--include', nargs='+', default='') # включить файлы с данным типом в синхронизацию
parser.add_argument('--exclude', nargs='+', default='') # исключить файлы с данным типом из синхронизации
parser.add_argument('--depth', nargs='+', default='') # вложенность
parser.add_argument('--db', nargs='+', default='') # путь к базе данных
parser.add_argument('--log', nargs='+', default='') # путь к файлу, где будут храниться логи
parser.add_argument('--id', nargs='+', default='') # синхронизация по id в БД

args = parser.parse_args()

db = DataBase('./test.db')
db.create_database()