import os
import json
from datetime import datetime

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
    
def log_state_transition(from_state, to_state, state_type, ticks=None, sub_dir=None, log_file=None):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "ticks": ticks,
        "from": str(from_state),
        "to": str(to_state)
    }
    if sub_dir:
        log_dir = f"logs/{sub_dir}/{state_type}_Logs"
    else:
        log_dir = f"logs/{state_type}_Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{state_type.lower()}_transitions.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_error(error,object=None):
    log_file = f"logs/error.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "error": f"What happened: {error}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_event(event,object=None):
    log_file = f"logs/event.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event": f"What happened: {event}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

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

def write_constant_to_file(filename, value):
    constants_dir = 'saves/constants'
    
    if not os.path.exists(constants_dir):
        os.makedirs(constants_dir)
        log_event(f"Directory created: {constants_dir}")

    file_path = os.path.join(constants_dir, filename)
    
    try:
        with open(file_path, 'w') as file:
            file.write(str(value))
        log_event(f"Constant '{value}' written to {file_path}")
    except Exception as e:
        log_error(f"Error writing to file: {e}")

def write_envar_to_file(filename, value):
    env_dir = 'environment'
    
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
        log_event(f"Directory created: {env_dir}")

    file_path = os.path.join(env_dir, filename)
    
    try:
        with open(file_path, 'w') as file:
            file.write(str(value))
        log_event(f"Constant '{value}' written to {file_path}")
    except Exception as e:
        log_error(f"Error writing to file: {e}")

def read_envar_from_file(filename):
    file_path = os.path.join('environment', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            log_event(f"File {file_path} does not exist.")
            return None
    except Exception as e:
        log_error(f"Error reading from file: {e}")
        return None

def read_constant_from_file(filename):
    file_path = os.path.join('saves/constants', filename)
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return file.read().strip()
        else:
            log_event(f"File {file_path} does not exist.")
            return None
    except Exception as e:
        log_error(f"Error reading from file: {e}")
        return None

def check_username():
    opt_in = read_constant_from_file('username')
    if opt_in is not None:
        return True
    else:
        return False
    
def check_recently_updated():
    updated = read_envar_from_file('recentlyupdated')
    if updated is not None:
        return True
    else:
        return False
    
def create_volume_files(default_volume):
    file_path = 'saves/constants'
    if not os.path.exists(f'{file_path}'):
        os.makedirs(f'{file_path}')
    
    if not os.path.exists(f"{file_path}/music_volume"):
        write_constant_to_file('music_volume',f'{default_volume}')
        log_event('Music volume file creation: music_volume file created')
    else:
        log_event('Music volume file creation: music_volume file exists')
    
    if not os.path.exists(f"{file_path}/sfx_volume"):
        write_constant_to_file('sfx_volume',f'{default_volume}')
        log_event('SFX volume file creation: sfx_volume file created')
    else:
        log_event('SFX volume file creation: sfx_volume file exists')

def draw_loading(font,window,text_string):
        import math
        t = window.get_current_time() / 500
        pulse = (math.sin(t) + 1) / 2  # 0 → 1

        dark = 40
        light = 255   

        fade_color = (
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
            int(dark + (light - dark) * pulse),
        )
        text = font.render(text_string, True, fade_color)
        rect = text.get_rect(center=(
            window.get_width() // 2,
            window.get_height() // 2
        ))
        window.blit(text, rect)