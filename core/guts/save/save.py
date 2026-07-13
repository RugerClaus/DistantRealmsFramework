import os
from systemlogging import log_event,log_error

class Save():
    def __init__(self,schema):
        self.game_save_path = "saves/gamedata/world.sav"
        self.save_schema = schema

    def write_envar(self,envar_name,value):
        log_event(f"Saving ENV value: '{value}' to: environment/{envar_name}")
        
        env_dir = 'environment'
    
        if not os.path.exists(env_dir):
            os.makedirs(env_dir)
            log_event(f"Directory created: {env_dir}")

        file_path = os.path.join(env_dir, envar_name)
        
        try:
            with open(file_path, 'w') as file:
                file.write(str(value))
            log_event(f"Constant '{value}' written to {file_path}")
        except Exception as e:
            log_error(f"Error writing to file: {e}")

        log_event(f"Saved ENV value: '{value}' to: environment/{envar_name}!")

    def write_constant(self,constant,value):
        log_event(f"Saving CONSTANT value: '{value}' to: saves/constants/{constant}")

        constants_dir = 'saves/constants'
    
        if not os.path.exists(constants_dir):
            os.makedirs(constants_dir)
            log_event(f"Directory created: {constants_dir}")

        file_path = os.path.join(constants_dir, constant)
        
        try:
            with open(file_path, 'w') as file:
                file.write(str(value))
            log_event(f"Constant '{value}' written to {file_path}")
        except Exception as e:
            log_error(f"Error writing to file: {e}")

        log_event(f"Saved CONSTANT value: '{value}' to: saves/constants/{constant}!")

    def write_save(self, data, file=None):
        if file:
            self.game_save_path = file
        with open(self.game_save_path, "w") as f:
            for file_key, mapped in self.save_schema.items():
                internal_key = mapped[0]

                if internal_key not in data:
                    continue

                value = data[internal_key]
                f.write(f"{file_key}={value}\n")
