from systemlogging import log_error

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
    log_error(f"Unknown asset: {asset}")
    return None

def get_colors(color):
    if color == "red":
        return (255,0,0)
    elif color  == "green":
        return (0,255,0)
    elif color == "blue":
        return (0,0,255)
    elif color == "purple":
        return (128,0,128)
    elif color == "black":
        return (0,0,0)
    elif color == "white":
        return (255,255,255)
    else:
        log_error("Can't find color!")
        return (128,128,128)
    
def audio_path(type):
    type = type.lower()
    if type == "music":
        return f"assets/sounds/music"
    elif type == "sfx":
        return f"assets/sounds/sfx"
    else:
        log_error("Can't find audio path!")
        return None

from core.guts.persistence.save import Save
save = Save()
def write_envar_to_file(filename,value):
    save.write_constant(filename,value)