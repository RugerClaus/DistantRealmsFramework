from helper import *
from core.game.save_schema import schema
class Load():
    def __init__(self):
        self.game_save_path = "saves/gamedata/world.sav"
        self.save_keys = ["WORLDSEED","PLAYERWORLDX","PLAYERWORLDY"]
        self.load_dict = {}

    def read_environment_variable(self,envar_name): 
        log_event(f"Reading contents in environment/{envar_name}")
        return read_envar_from_file(envar_name) # returns a string
    
    def read_constant(self,constant): 
        log_event(f"Reading contents in saves/constants/{constant}")
        return read_constant_from_file(constant)
    
    def load_game_save(self):
        if os.path.exists(self.game_save_path):
            with open(self.game_save_path, "r") as f:
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