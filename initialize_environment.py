from config import config
with open("saves/constants/n","a+") as application_name:
    application_name.write(config.get("TITLE"))