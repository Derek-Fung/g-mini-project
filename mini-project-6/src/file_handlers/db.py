import pymysql
import random

class DbFileHelper:
    def __init__(self) -> None:
        pass
    
    def get_filecontents(self, file_name, default_data):
        with open(file_name, 'a') as f: # create file if not exist
            pass
        with open(file_name, 'r+') as f: # read the file, use r+, do not erase existing data
            f_list = f.readlines()
            f_list[:] = [x.replace("\n", "").strip() for x in f_list if x.replace("\n", "").strip()]
            if len(f_list) == 0:      # if no content, write the defualt data into the file
                content = ''
                for item in default_data:
                    content += f'{item}\n'
                f.write(content)             
            else:                            # if aleady have content, override the default data
                default_data[:] = f_list
        return default_data  
