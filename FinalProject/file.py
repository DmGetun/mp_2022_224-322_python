import os
from abc import abstractmethod
import shutil
import hashlib

class FileReader:
    
    def __init__(self, path):
        self.path = path
        
    
    def _read_info(self):
        return os.stat(self.path)
            

    def get_info(self):
        stat = self._read_info()
        hash = self.get_hash()
            
        return stat, hash
            
    def synchronize(self, dest_path):
        shutil.copy2(self.path, dest_path)
        
        
    def get_hash(self):
        with open(self.path, 'rb') as f:
            data = f.read()
            digest = hashlib.sha256(data)
        
        return digest.hexdigest()
        
        
    
    
    
        