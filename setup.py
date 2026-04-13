import shutil
import os

example_config = "example.config.py"
config_file = "config.py"

if not os.path.exists(example_config):
    print(f"Error: '{example_config}' does not exist in this directory.")
    exit(1)

shutil.copyfile(example_config, config_file)

print(f"'{config_file}' has been created from '{example_config}'.")
