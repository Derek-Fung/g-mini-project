import csv

class CsvFileHelper:
    def __init__(self) -> None:
        pass

    def get_filecontents(self, file_name, default_data):
        with open(file_name, 'a') as f: # create file if not exist
            pass
        with open(file_name, 'r+', newline='') as f: 
            reader = csv.DictReader(f)
            f_list = [row for row in reader]     
            if len(f_list) == 0:      # if no content, write the defualt data into the file
                writer = csv.writer(f, delimiter=',')
                # instruct the write to write a row
                writer.writerow([key for key in default_data[0].keys()])
                [writer.writerow([y for x, y in dic.items()]) for dic in default_data]            
            else:                            # if aleady have content, override the default data
                default_data[:] = f_list
        return default_data  

 
        
    def write_filecontents(self, file_name, update_data):
        f_list = [row for row in update_data] 
        with open(file_name, 'w+', newline='') as f: # Use w+, erase existing data and write whole new set of data  
            if len(f_list) == 0:
                pass # The file was empty by w+ in with open().
            else:
                writer = csv.writer(f, delimiter=',')
                writer.writerow([key for key in update_data[0].keys()])
                [writer.writerow([y for x, y in dic.items()]) for dic in update_data]  
        return update_data

        

             