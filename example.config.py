import platform

config = {
    "TITLE": "My app -",
    "VERSION": "1.0.0-beta",
    "FRAMEWORK VERSION": "0.8.0-alpha",
    "OS": platform.system(),
    "OSV": platform.version(),
    "OSR": platform.release(),
    "UPDATE_ZIP_NAME": "snowblitz_update_latest.zip",
    "UPDATER_WINDOWS": "updater.exe",
    "UPDATER_LINUX": "updater",
    "UPDATER_VERSION": "0.0.2",
    "WINDOW_BACKEND": "backcompat",
    "NSTATURL": "https://snowblitz.net",
    "SPLASHSCREEN": True,
    "API_KEY": "",
    "API": {
        "LEADERBOARD": "",
        "REGISTRATION_URL": "",
        "LOGIN_URL": "",
        "UPDATE_SCORE": "",
        "UPDATE_FILE_URL": "",
        "CURRENT_VERSION": "",
        "CREATE_SESSION": "",
    },
        "ASSETS": {
        "title": "assets/images/main/title.png",
        "default_font": "assets/font/OpenSansPX.ttf",
        "bold": "assets/font/OpenSansPXBold.ttf",

        "splashpt1": "assets/images/main/splashpt1.png",
        "splashpt2": "assets/images/main/splashpt2.png",
        "splashpt3": "assets/images/main/splashpt3.png",
        "splashpt4": "assets/images/main/splashpt4.png",
        "splashpt5": "assets/images/main/splashpt5.png",
        

        "splash1": "assets/sounds/sfx/splash1.ogg",
        "splash2": "assets/sounds/sfx/splash2.ogg",
        "splash3": "assets/sounds/sfx/splash3.ogg",
        "splash4": "assets/sounds/sfx/splash4.ogg",
        "splash5": "assets/sounds/sfx/splash5.ogg",

        "button_clicked": "assets/sounds/sfx/button_clicked.mp3",

        "linux_icon": "assets/images/build/linux.png",
        "windows_icon": "assets/images/build/windows.ico",

        #shaders
        "v": "shaders/v.glsl",
        "f": "shaders/f.glsl",
        "texturev": "shaders/texturev.glsl",
        "texturef": "shaders/texturef.glsl",
        "cube": "shaders/cube.glsl",
        "plane": "shaders/plane.glsl",
        "rectpulse": "shaders/rectpulse.glsl",
        "fcellshader": "shaders/fcellshader.glsl",
        "roundedrectf": "shaders/roundedrectf.glsl",
        "roundedrectv": "shaders/roundedrectv.glsl"
    }
}