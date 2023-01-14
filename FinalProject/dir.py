import os 


class Dir:
    def __init__(self, path):
        self.path = path
        
    def count(self):
        counter = 0
        for _,_,_ in os.walk(self.path):
            counter += 1
            
        return counter
    
    