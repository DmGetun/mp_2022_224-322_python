import sqlite3
import os 
from datetime import datetime
import time

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
                stmode datetime, --права пользователя
                atime datetime, --время последнего доступа к файлу
                mtime datetime, --время последнего изменения файла
                ctime datetime, --время последнего изменения прав доступа или владельца
                content TEXT --содержимое файла
            );
        '''
        
        cursor.execute(query)
        con.commit()
        
        query = f'''
            CREATE TABLE IF NOT EXISTS {sync_info_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sync_time datetime,
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
        con.commit()
        cursor.close()
        con.close()
    
    
    def get_tables(self):
        return self.cursor.execute("select name from sqlite_master where type='table';").fetchall()
    
    
    def insert_file_info(self, name, stmode, atime, mtime, ctime, content):
        con = sqlite3.connect(self.path)
        con.text_factory = str
        cursor = con.cursor()
        
        stmode = datetime.fromtimestamp(stmode).strftime('%Y-%m-%d %H:%M:%S')
        atime = datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S')
        mtime = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        ctime = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
        
        query = f'''
            INSERT INTO {file_info_table} (filename, stmode, atime, mtime, ctime, content) VALUES
            ('{name}', '{stmode}', '{atime}', '{mtime}', '{ctime}', ' ');
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
            INSERT INTO {sync_info_table} (sync_id, sync_time,source_path, destination_path, file_id) values 
            ({sync_id}, datetime('now') ,'{source_path}', '{destination_path}', {file_id})
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
            order by mtime DESC
        '''
        cursor.execute(query)
        
        data = cursor.fetchone()
        return data[0] if data is not None else None
    
    def get_all_sync(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            SELECT sync_id, sync_time, source_path, destination_path, filename FROM {sync_info_table} s
            LEFT JOIN {file_info_table} f
            ON s.file_id = f.id
        '''
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        self.close_db(con,cursor)
        
        return data
    
    def get_sync_on_id(self, id):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            SELECT filename, destination_path
            FROM {sync_info_table} s
            left join {file_info_table} f
            on s.file_id = f.id
            WHERE s.sync_id = {id}
        '''
        cursor.execute(query)
        
        return cursor.fetchall()
    
    
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
    
    
    def get_file_on_name(self, filename):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        query = f'''
            SELECT filename from {file_info_table}
            WHERE filename = '{filename}'
        '''
        cursor.execute(query)
        filename_db = cursor.fetchone()
        self.close_db(con,cursor)
        
        if filename_db is None:
            return None 
        
        return filename_db[0]
    
    def update_file(self, filename, stmode, atime, mtime, ctime, content):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        
        stmode = datetime.fromtimestamp(stmode).strftime('%Y-%m-%d %H:%M:%S')
        atime = datetime.fromtimestamp(atime).strftime('%Y-%m-%d %H:%M:%S')
        mtime = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        ctime = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
        
        query = f'''
            UPDATE {file_info_table} 
            SET
                filename='{filename}',
                stmode='{stmode}',
                atime='{atime}',
                mtime='{mtime}',
                ctime='{ctime}',
                content=' '
            WHERE filename='{filename}';
        '''
        
        cursor.execute(query)
        
        self.close_db(con, cursor)
        
    
        
    
        