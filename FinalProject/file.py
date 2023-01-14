import os 

class File:
    
    def __init__(self, path):
        self.path = path
        
    
    def open(self):
        with open(self.path) as f:
            stat = os.stat(self.path)
        