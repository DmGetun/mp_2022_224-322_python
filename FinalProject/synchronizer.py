import os
from db import DataBase
from logger import Logger
from file import FileReader
from tqdm import tqdm
import shutil



class Synchronizer:
    
    def __init__(self, files, src, dst, log, db:DataBase, id):
        self.files = files
        self.src = src 
        self.dst = dst
        self.log = log
        self.db = db
        self.id = id

        
    def synchronize(self):
        
        if not os.path.exists(self.dst):
            os.mkdir(self.dst)
        
        if self.id is not None:
            log_message = f"Начата синхронизация с id={self.id}: {self.src} -> {self.dst}"
            Logger.log(log_message, self.log)
            self.synchronize_on_id()
        else:
            log_message = f"Начата новая синхронизация {self.src} -> {self.dst}"
            Logger.log(log_message, self.log)
            self.new_synchronize()
        
        log_message = f"Синхронизация {self.src} -> {self.dst} закончена"
        Logger.log(log_message, self.log)
    
    
    def new_synchronize(self):
        sync_id = self.db.get_last_sync_id()
        if self.id is not None:
            sync_id += 1

        for file in tqdm(self.files):
            reader = FileReader(file)
            stat, content = reader.get_info()
            file_id = self.db.insert_file_info(
                file,
                stat.st_mode,
                stat.st_atime,
                stat.st_mtime,
                stat.st_ctime,
                content
            )
            self.db.insert_sync_info(sync_id,self.src,self.dst,file_id)
            mtime_from_db = self.db.get_last_modified_time(file)
            if self.is_updateable_file(stat.st_mtime ,mtime_from_db):
                self.recursive_copy(file,self.dst)
            else:
                log_message = f"Файл {file} уже синхронизирован с {self.dst}"
                Logger.log(log_message, self.log)
    
    def recursive_copy(self, src, dest: str):
        part_src: str = src.removeprefix(self.src)
        file_name = os.path.basename(src)
        part_src: str = part_src.removesuffix(file_name)
        part_src = part_src.removeprefix('\\')

        if os.path.isdir(part_src) and len(part_src) >= 0:
            if not os.path.exists(os.path.join(dest, part_src)):
                os.makedirs(os.path.join(dest, part_src))

        path_for_copy = os.path.join(dest,part_src,file_name) if len(part_src) >= 0 else os.path.join(dest,file_name)
    
        try:
            shutil.copy2(src, path_for_copy)
            log_message = f"Файл {src} был синхронизирован с {path_for_copy}"
            Logger.log(log_message, self.log)
        except shutil.SameFileError:
            return
            

    def is_updateable_file(self, mtime, mtime_from_db):
        return float.hex(mtime) != float.hex(mtime_from_db)
        

    def synchronize_on_id(self):
        sync_from_db = self.db.get_sync_on_id(self.id)
        
        files = [file[0] for file in sync_from_db]
        self.files = files
        
        dest_path = sync_from_db[0][1]
        self.dst = dest_path
        
        self.new_synchronize()
        
    
