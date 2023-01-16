
class Logger():
    
    @staticmethod
    def log(text, path):
        with open(path,'ra',encoding='utf-8') as f:
            f.write(text) 
        