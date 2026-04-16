from helper import log_event,write_envar_to_file,write_constant_to_file
class Save():
    def __init__(self,schema):
        self.game_save_path = "saves/gamedata/world.sav"
        self.save_schema = schema

    def write_environment_variable(self,envar_name,value):
        log_event(f"Saving ENV value: '{value}' to: environment/{envar_name}")
        write_envar_to_file(envar_name,value)
        log_event(f"Saved ENV value: '{value}' to: environment/{envar_name}!")

    def write_constant(self,constant,value):
        log_event(f"Saving CONSTANT value: '{value}' to: saves/constants/{constant}")
        write_constant_to_file(constant,value)
        log_event(f"Saved CONSTANT value: '{value}' to: saves/constants/{constant}!")

    def write_game_save(self, data):
        with open(self.game_save_path, "w") as f:
            for file_key, mapped in self.save_schema.items():
                internal_key = mapped[0]

                if internal_key not in data:
                    continue

                value = data[internal_key]
                f.write(f"{file_key}={value}\n")
