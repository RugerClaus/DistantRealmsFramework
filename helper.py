from systemlogging import log_error
import math,sys

from pathlib import Path
from config import config

def asset(name):
    path = config.get("ASSETS", {}).get(name)

    if path is None:
        return None

    return resolve_path(path)

def resolve_path(filename):
    path = Path(filename)

    if path.is_absolute():
        return path

    # Source tree / normal execution
    if path.exists():
        return path

    # Packaged application
    if getattr(sys, "frozen", False):
        packaged_path = Path(sys.executable).resolve().parent / "distantrealms" / path

        if packaged_path.exists():
            return packaged_path

    return path
    
def audio_path(type):
    type = type.lower()
    if type == "music":
        return f"assets/sounds/music"
    elif type == "sfx":
        return f"assets/sounds/sfx"
    else:
        log_error("Can't find audio path!")
        return None

from core.engine.persistence.save import Save
save = Save()
def write_envar_to_file(filename,value):
    save.write_constant(filename,value)

def sine(current_time):
    t = current_time / 1000
    pulse = (math.sin(t) + 1) / 2
    return pulse

def load_file(filename):
    path = resolve_path(filename)

    with open(path, "r", encoding="utf-8") as file:
        return file.read()