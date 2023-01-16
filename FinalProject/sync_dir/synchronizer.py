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
            self.synchronize_on_id()
        else:
            self.new_synchronize()
    
    
    def new_synchronize(self):
        for file in tqdm(self.files):
            reader = FileReader(file)
            stat, content = reader.get_info()
            sync_id = self.db.get_last_sync_id() + 1
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
            flag = self.is_updateable_file(stat.st_mtime ,mtime_from_db)
            if self.is_updateable_file(stat.st_mtime ,mtime_from_db):
                self.recursive_copy(file,self.dst)
    
    def recursive_copy(self, src, dest: str):
        part_src: str = src.removeprefix(self.src)
        file_name = os.path.basename(src)
        part_src: str = part_src.removesuffix(file_name)
        part_src = part_src.removeprefix('\\')
        if os.path.isdir(part_src) and len(part_src) >= 0:
            if not os.path.exists(os.path.join(dest, part_src)):
                os.makedirs(os.path.join(dest, part_src))
        
        path_for_copy = ''
        
        if len(part_src) >= 0:
            path_for_copy = os.path.join(dest,part_src,file_name)
        else:
            path_for_copy = os.path.join(dest,file_name)
        
        
        try:
            shutil.copy2(src, path_for_copy)
        except shutil.SameFileError:
            return
            

    def is_updateable_file(self, mtime, mtime_from_db):
        return float.hex(mtime) != float.hex(mtime_from_db)
        

    def synchronize_on_id(self, db):
        pass
        
    
