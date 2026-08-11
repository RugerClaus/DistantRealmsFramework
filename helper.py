from systemlogging import log_error
import math

def asset(asset):
    if asset == "title":
        return "assets/images/main/title.png"
    elif asset == "default_font":
        return 'assets/font/OpenSansPX.ttf'
    elif asset == "splashpt1":
        return "assets/images/main/splashpt1.png"
    elif asset == "splashpt2":
        return "assets/images/main/splashpt2.png"
    elif asset == "linux_icon":
        return "assets/images/build/linux.png"
    elif asset == "windows_icon":
        return "assets/images/build/windows.ico"
    elif asset == "multiplierupgrade":
        return "assets/images/main/multiplierupgrade.png"
    elif asset == "clock":
        return "assets/images/main/clock.png"
    
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