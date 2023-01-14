import sqlite3
import os 

class DataBase:
    
    def __init__(self, path):
        self.path = path
        
    
    def create_database(self):
        if not os.path.exists(self.path):
            answer = input('Данной базы данных не существует. Создать новую базу данных?[y]: ')
            if answer != 'y':
                exit()
        
        con = sqlite3.connect(self.path)
        self.con = con
        self.cursor = con.cursor()
        
    def create_tables(self):
        
        query = '''
            CREATE TABLE file_info (
                id INTEGER PRIMAKY KEY NOT NULL,
                filename VARCHAR(255),
                stmode -- права пользователя
                atime --время последнего доступа к файлу
                mtime --время последнего изменения файла
                ctime --время последнего изменения прав доступа или владельца
            );
        '''
        
        
        query = '''
            CREATE TABLE synchronize_info (
                id INTEGER PRIMARY KEY NOT NULL,
                sync_id INTEGER NOT NULL,
                source_path VARCHAR(255),
                destination_path VARCHAR(255),
                file_id INTEGER
                
                FOREIGN KEY(file_id) REFERENCES file_info(id)
                
            );
        '''
        
    
        
    
        