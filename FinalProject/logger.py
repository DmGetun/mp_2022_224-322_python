from datetime import datetime


class Logger():
    
    @staticmethod
    def log(text, path):
        now = datetime.now() 
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{time}] {text}\n"
        with open(path,'a',encoding='utf-8') as f:
            f.write(message)
        