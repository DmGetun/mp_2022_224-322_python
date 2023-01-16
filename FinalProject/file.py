import os
from abc import abstractmethod
import shutil 

class FileReader:
    
    def __init__(self, path):
        self.path = path
        
    
    def _read_info(self):
        return os.stat(self.path)
            

    def get_info(self):
        stat = self._read_info()
        with open(self.path, 'rb') as f:
            content = f.read()
            
        return stat, content
            
    def synchronize(self, dest_path):
        shutil.copy2(self.path, dest_path)
        
        
    
    
    
        