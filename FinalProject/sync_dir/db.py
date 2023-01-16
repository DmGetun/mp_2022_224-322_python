import sqlite3
import os 

file_info_table = 'file_info'
sync_info_table = 'synchronize_info'

class DataBase:
    
    def __init__(self, path):
        self.path = path
        
    
    def create_database(self):
        if not os.path.exists(self.path):
            answer = input('Данной базы данных не существует. Создать новую базу данных?[y]: ')
            if answer != 'y':
                exit()
        
        con = sqlite3.connect(self.path)
        con.close()
        
    def create_tables(self):
        
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            CREATE TABLE IF NOT EXISTS {file_info_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename VARCHAR(255),
                stmode REAL, --права пользователя
                atime REAL, --время последнего доступа к файлу
                mtime REAL, --время последнего изменения файла
                ctime REAL, --время последнего изменения прав доступа или владельца
                content TEXT --содержимое файла
            );
        '''
        
        cursor.execute(query)
        con.commit()
        
        query = f'''
            CREATE TABLE IF NOT EXISTS {sync_info_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_id INTEGER NOT NULL,
                source_path VARCHAR(255),
                destination_path VARCHAR(255),
                file_id INTEGER,
                
                FOREIGN KEY(file_id) REFERENCES file_info(id)  
            );
        '''
        cursor.execute(query)
        
        con.commit()
        
        cursor.close()
        con.close()
        
    
    def close_db(self, con,cursor):
        cursor.close()
        con.close()
    
    
    def get_tables(self):
        return self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
    
    
    def insert_file_info(self, name, stmode, atime, mtime, ctime, content):
        con = sqlite3.connect(self.path)
        con.text_factory = str
        cursor = con.cursor()
        
        query = f'''
            INSERT INTO {file_info_table} (filename, stmode, atime, mtime, ctime, content) VALUES
            ('{name}', {stmode}, {atime}, {mtime}, {ctime}, ' ');
        '''
        cursor.execute(query)
        con.commit()
        
        cursor.execute(f'select last_insert_rowid() from {file_info_table};')
        result = cursor.fetchone()
        self.close_db(con, cursor)
        return result[0]
    
    def insert_sync_info(self, sync_id, source_path, destination_path, file_id):
        
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        query = f'''
            INSERT INTO {sync_info_table} (sync_id, source_path, destination_path, file_id) values 
            ({sync_id}, '{source_path}', '{destination_path}', {file_id})
        '''
        cursor.execute(query)
        con.commit()
        self.close_db(con,cursor)
        
    def get_last_modified_time(self,filename):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            SELECT mtime
            FROM {file_info_table}
            WHERE filename = '{filename}'
        '''
        cursor.execute(query)
        
        return cursor.fetchone()[0]
        
    
    def get_stat_on_filename(self,filename):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            SELECT stmode, atime, mtime,ctime
            FROM {file_info_table}
            WHERE filename = '{filename}'
        '''
        cursor.execute(query)
        
        return cursor.fetchone()
        
    
    def get_files_without_content(self):
        
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        query = f'''
            SELECT filename,stmode,atime,mtime,ctime from {file_info_table} f
        '''
        cursor.execute(query)
        data = cursor.fetchall()
        
        self.close_db(con,cursor)
        
        return data 
    
    def get_last_sync_id(self):
        
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            select MAX(sync_id) from {sync_info_table};
        '''
        cursor.execute(query)
        id = cursor.fetchone()
        self.close_db(con,cursor)
        return id[0] if id[0] is not None else 1
        
    
        
    
        