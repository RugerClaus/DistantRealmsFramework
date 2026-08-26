import platform

config = {
    "TITLE": "Snow Blitz Beta prelease 1 -",
    "VERSION": "1.0.0-beta",
    "FRAMEWORK VERSION": "0.6.1-alpha",
    "OS": platform.system(),
    "OSV": platform.version(),
    "OSR": platform.release(),
    "UPDATE_ZIP_NAME": "snowblitz_update_latest.zip",
    "UPDATER_WINDOWS": "updater.exe",
    "UPDATER_LINUX": "updater",
    "UPDATER_VERSION": "0.0.2",
    "WINDOW_BACKEND": "pygame",
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

        "splashpt1": "assets/images/main/splashpt1.png",
        "splashpt2": "assets/images/main/splashpt2.png",

        "splash1": "assets/audio/sfx/splash1.ogg",
        "splash2": "assets/audio/sfx/splash2.ogg",

        "linux_icon": "assets/images/build/linux.png",
        "windows_icon": "assets/images/build/windows.ico",
    }
}