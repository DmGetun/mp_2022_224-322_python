import argparse
from db import DataBase
from dir import Dir 
from file import FileReader
from synchronizer import Synchronizer
import os
from db import DataBase
from prettytable import PrettyTable

p = PrettyTable()
p.field_names = ['sync_id', 'source', 'destination', 'filename']

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
parser.add_argument('--show', nargs=argparse.REMAINDER) # показать существующие синхронизации

args = parser.parse_args()

if len(args.include) > 0 and len(args.exclude) > 0:
    raise IllegalArgumentError('Нельзя выполнить синхронизацию с флагами include и exclude одновременно')

if len(args.source) > 0 or len(args.destination) > 0:
    if len(args.id) > 0:
        raise IllegalArgumentError("Невозможно выполнить синхронизацию с указанным флагом --id и --source или --destination вместе")

def create_bat(src, dest, include, exclude, depth, id, log):
    command = "python C:\Универ\Современные технологии программирования\питон\mp_2022_224-322_python\FinalProject\main.py"
    if src is not None:
        command += f' --source {src}'
    if dest is not None:
        command += f' --destination {dest}'
    if include is not None:
        command += f' --include {include}'
    if exclude is not None:    
        command += f' --exclude {exclude}'
    if depth is not None:
        command += f' --depth {depth}'
    if id is not None:
        command += f' --id {id}'
    if log is not None:
        command += f' --log {log}'
        
    command += '\n pause'
        
    with open('synchronize.bat','w',encoding='utf-8') as w:
        w.write(command)
    

db = DataBase('./test.db')
db.create_database()
db.create_tables()

src_path = args.source[0] if len(args.source) > 0 else '.'
dest_path = args.destination[0] if len(args.destination) > 0 else '.'
include_files = args.include if len(args.include) > 0 else None
exclude_files = args.exclude if len(args.exclude) > 0 else None
depth = args.depth[0] if len(args.depth) > 0 else None
id = args.id[0] if len(args.id) > 0 else None
log = args.log[0] if len(args.log) > 0 else './log.txt'


if args.show is not None:
    all_sync = db.get_all_sync()
    for info in all_sync:
        p.add_row(info)
    print(p)
    exit()    


# ДЛЯ ТЕСТОВ!

#src_path = "D:\\test_sync"
#dest_path = "D:\dir_to_sync"

#src_path = os.path.join(os.path.abspath(src_path))
#dest_path = os.path.join(os.path.abspath(dest_path))
#exclude_files = ['pdf']
#id = 1

create_bat(src_path, dest_path, include_files, exclude_files, depth, id, log)   

files = Dir.recursive_walk(src_path,0,depth,include_files,exclude_files)

synchronizer = Synchronizer(files, src_path, dest_path, log, db, id)
synchronizer.synchronize()
