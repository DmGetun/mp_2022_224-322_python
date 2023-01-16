import os 
import file
import pathlib

class Dir:
    
    @staticmethod
    def recursive_walk(
            src_path: str, 
            depth: int, 
            max_depth: int, 
            include_types: list=None, 
            exclude_types: list=None) -> list:
        files = []
        
        if max_depth is not None and depth >= max_depth:
            return
    
        for file in os.listdir(src_path):
            file_path = os.path.join(os.path.abspath(src_path), file)
            _, file_ext = os.path.splitext(file_path)
            
            if os.path.isfile(file_path):
                if include_types is not None and file_ext in include_types:
                    files.append(file_path)
                elif exclude_types is not None and file_ext not in exclude_types:
                    files.append(file_path)
                elif exclude_types is None and include_types is None:
                    files.append(file_path)
                    
            else:
                res = Dir.recursive_walk(file_path, depth+1, max_depth, include_types, exclude_types)
                files.extend(res)
                
        return files
    
    