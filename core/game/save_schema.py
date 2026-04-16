# enter your save keys here 
# the format is KEY=VALUE in the save file system
# so you must follow this example schema when picking your naming

# schema = {
#     "WORLDSEED": ("seed", int),
#     "PLAYERWORLDX": ("player_world_x", int),
#     "PLAYERWORLDY": ("player_world_y", int),
# }

# as you can see, you just format your key with your value so the save system know what to load
# you just store your own values whatever they may be and the save/load system will take care of you!


schema = {
    "WORLDSEED": ("seed", int),
    "PLAYERWORLDX": ("player_world_x", float),
    "PLAYERWORLDY": ("player_world_y", float),
}