from helper import *
class Load():
    def __init__(self):
        pass

    def read_environment_variable(self,envar_name): 
        log_event(f"Reading contents in environment/{envar_name}")
        return read_envar_from_file(envar_name) # returns a string
    
    def read_constant(self,constant): 
        log_event(f"Reading contents in saves/constants/{constant}")
        return read_constant_from_file(constant)