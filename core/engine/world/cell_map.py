from core.util.colors import *
cell_data_map = {
    0: {
        "name": "empty",
        "color": None,
        "properties": {
            "collidable": False,
            "receives_light": False
        }
    },

    1: {
        "name": "grass",
        "color": green,
        "properties": {
            "collidable": False,
            "receives_light": True
        }
    },

    2: {
        "name": "yellow",
        "color": yellow,
        "properties": {
            "collidable": False,
            "receives_light": False
        }
    },

    3: {
        "name": "cloud",
        "color": white,
        "properties": {
            "collidable": False,
            "receives_light": True
        }
    },
    4: {
        "name": "dirt",
        "color": saddle_brown,
        "properties": {
            "collidable": False,
            "receives_light": False
        }
    },
    5: {
        "name": "snow",
        "color": snow,
        "properties": {
            "collidable": False,
            "receives_light": True
        }
    }
}