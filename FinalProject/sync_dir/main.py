import argparse
from db import DataBase
from dir import Dir 
from file import FileReader
from synchronizer import Synchronizer
import os 

class IllegalArgumentError(ValueError):
    pass

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

if len(args.include) > 0 and len(args.exclude) > 0:
    raise IllegalArgumentError('Нельзя выполнить синхронизацию с флагами include и exclude одновременно')

db = DataBase('./test.db')
db.create_database()
db.create_tables()

src_path = args.source[0] if len(args.source) > 0 else '.'
dest_path = args.destination[0] if len(args.destination) > 0 else '.'
include_files = args.include[0] if len(args.include) > 0 else None
exclude_files = args.exclude[0] if len(args.exclude) > 0 else None
depth = args.depth[0] if len(args.depth) > 0 else None
id = args.id[0] if len(args.id) > 0 else None
log = args.log[0] if len(args.log) > 0 else None


# ДЛЯ ТЕСТОВ!
src_path = os.path.join(os.path.abspath(src_path))
dest_path = os.path.join(os.path.abspath(src_path),'sync_dir')


files = Dir.recursive_walk(src_path,0,depth,include_files,exclude_files)

synchronizer = Synchronizer(files, src_path, dest_path, log, db, id)
synchronizer.synchronize()

