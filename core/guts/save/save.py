from helper import log_event,write_envar_to_file,write_constant_to_file
class Save():
    def __init__(self):
        pass

    def write_environment_variable(self,envar_name,value):
        log_event(f"Saving ENV value: '{value}' to: environment/{envar_name}")
        write_envar_to_file(envar_name,value)
        log_event(f"Saved ENV value: '{value}' to: environment/{envar_name}!")

    def write_constant(self,constant,value):
        log_event(f"Saving CONSTANT value: '{value}' to: saves/constants/{constant}")
        write_constant_to_file(constant,value)
        log_event(f"Saved CONSTANT value: '{value}' to: saves/constants/{constant}!")