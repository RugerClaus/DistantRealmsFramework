import os
from systemlogging import log_event,log_error
from application.save_schema import schema

class Load():
    def __init__(self):
        self.load_dict = {}

    def read_envar(self,envar_name): 
        file_path = os.path.join('environment', envar_name)
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    return file.read().strip()
            else:
                log_error(f"File {file_path} does not exist.")
                return None
        except Exception as e:
            log_error(f"Error reading from file: {e}")
            return None
    
    def read_constant(self,constant): 
        file_path = os.path.join('saves/constants', constant)
    
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    return file.read().strip()
            else:
                log_error(f"File {file_path} does not exist.")
                return None
        except Exception as e:
            log_error(f"Error reading from file: {e}")
            return None
    
    def load_save(self,file="app.sav'"):
        app_save_path = f"saves/appdata/{file}.sav"
        if os.path.exists(app_save_path):
            with open(app_save_path, "r") as f:
                for line in f:
                    line = line.strip()
                    
                    if "=" not in line:
                        log_error(f"Error in line: {line}. Line is missing ")

                    key, value = line.split("=", 1)
                    
                    mapped = schema.get(key)
                    if mapped:
                        internal_key, converter = mapped
                        self.load_dict[internal_key] = converter(value)
            return self.load_dict
        else:
            return None