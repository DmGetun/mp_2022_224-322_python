import os 

for current_dir, dirs, files in os.walk("C:\Универ\Логика и алгоритмы"):
    for file in files:
        print(current_dir, dirs, files)