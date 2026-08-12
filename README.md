# Welcome to the Distant Realms Framework for Developing Applications with Python

## Introduction
- Distant Realms is a Python application framework and tooling ecosystem for building games and interactive applications. Containing support for rendering, audio, input, simple networking as well as a ready built WYSIWYG ui editor that outputs to a format the engine can read directly. Below you will learn how to make games and other applications using Distant Realms

- Distant Realms is designed around convenience without lock-in.

- The framework provides high-level systems for common application needs, but those systems are built on straightforward underlying APIs. You can use as much or as little of the framework as your application requires.

NOTE: ALL EXAMPLE SECTIONS START WITH A NUMBER LIKE THIS: [01] +. When I refer to an example, I will refer to its number.

## Dependencies

This project has a few dependencies. The only third-party assets are the fonts in `assets/font`.

It uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. See `LICENSE.txt` in the `assets/font` directory for details.

There is no requirements.txt because there are only four dependencies.

## Setup

From the root directory, run:

```bash setup.sh```

Once this has run, you should be all set to run the program using:

To start the program in normal most with developer mode off:

```python3 main.py```

To start the program with developer mode on:

```python3 main.py --dev```

To skip the splash screen and start the program with developer mode on:

```python3 main.py --devg```

For windows use:
 ```python main.py --flags```

# Project Structure

When you create an application with Distant Realms, the framework provides a directory structure for separating application code, framework/engine systems, data on the disk, assets, and tooling.

You do not need to understand every single directory or class to get started. Think of this a bit like Laravel or another large application framework, where your primary work takes place in a few, very specific directories.

    DistantRealmsFramework/
    ├── assets/              # Application assets
    ├── core/                # Framework and application systems
    ├── enginepersistence/   # Framework-managed data including UI files
    ├── environment/         # Environment-specific data
    ├── saves/               # User/application save data
    ├── logs/                # Runtime logs
    ├── tools/               # A directory created by installers if it does not exist, for example "install_editor_[windows|linux].sh" creates this directory
    ├── main.py              # System application entry point
    ├── config.py            # Application/framework configuration
    ├── setup.sh             # Framework setup
    ├── buildlinux.sh        # Linux build script
    ├── buildwindows.sh      # Windows build script
    ├── buildmacos.sh        # macOS build script
    └── README.md            # Framework documentation

You'll be doing most of your work inside the ```core/``` directory in ``` core/application```. Inside that directory, you'll find ```application.py``` containing a class called ```Application```. This class is where all your code goes, and anything else you add, including directories and modules, should remain beneath ```core/application```, unless you're creating state machines, in which case follow the documentation near the bottom of the README.

The ```core/``` directory is really where all the magic is happening, so I'm going to give a basic rundown on each directory inside of it:
    
    core/
    ├── application/     # Your application code and application-facing APIs
    ├── experimental/    # Experimental and in-development framework features
    ├── guts/            # Framework internals and core runtime services
    ├── loading/         # Boot, loading screen, and application loading systems
    ├── state/           # State machine definitions and state management
    ├── ui/              # Framework UI system and widgets
    └── util/            # Shared utility classes, helpers, and supporting functionality

For example, ```core/util``` contains the ```DebugOverlay``` class in ```core/util/debugoverlay.py```. This is the service container for all the functionality of the debug overlay. This is the perfect example of a file, you'll likely never need to think about. The same goes for mostly anything outside of ```core/application```. You may find yourself using the state system as well, and you'll primarily be working in, and creating your state machines in ```core/state/ApplicationLayer/```. This will all be explained under the State Machine section of the docs.

# About 3rd party dependencies:

Pygame-ce provides the backend for creating a window, drawing, audio, and input, as well as some of its time functions. 
The files that use it are as follows:

    ```
    -core/engine/window.py
    -core/engine/audioengine.py
    -core/engine/input/inputmanager.py
    -core/engine/input/keys.py
    -core/engine/time.py
    ```

A simple API is provided for working with all of these functionalities using the System services container. More below.

Mutagen provides the File function for getting attributes of WAV files for all inlcuded music tracks. The audio system included with this framework allows you to arbitrarily drag in your audio files, and run them with ```system.sound.play_music("tile of your track"). Mutagen aids in accomplishing this user-friendly feature!

Requests is used for networking capabilities. There are built in assumptions for authentication as well as ensuring the system is online, and having fallbacks for if it is not online.

Finally PyInstaller is used by the built in buildscripts (buildlinux.sh,buildwindows.sh,buildmacos.sh) to package executables of whatever program you decide to make with the framework.

# Included tools of the ecosystem

This project is becoming its own distribution ecosystem for making games, as I've intended from the beginning. Currently there is one major external, self-hosted tool for the framework and that is the Distant Realms Editor. You can install and run the Distant Realms Editor at any time by running:
 ```bash install_editor_[windows|linux].sh```

The Distant Realms Editor is a self-hosted application built on this very same framework. I presents the user with a graphical interface for creating UIs for your applications and games. Making a main menu has never been easier, as you can learn to use the drag and drop interface to create complex, rich, and highly functional user interfaces.

# Getting Started Making Games and Apps

To start off you'll be wanting to work in core/application/application.py. Here you will immediately find the patterns that the engine expects you to follow.

The core functions for frame by frame operations are as follows:

Establishing frame by frame event handling for your application: 

    ```handle_event(event,command)```

Establishing the update loop. This is where you'll pass all your non-drawing updates to the program that you want to run every frame:

    ```update()```

Establishing all rendering functions by convention. All your blits should be here:

    ```draw()```

To get started here are some of the core APIs for controlling things like drawing things to the screen, playing music and sound effects, and handling user input as well as how to use the command registration system:

The way the program is invoked is by creating two singletons. A System, which is an object that acts as a services container for core systems (rendering,audio,input,networking,and initializing applications). This does not establish the loop. 

The second singleton created is a Runtime object which contains a method called run() that when invoked begins an infinite while loop that runs every frame until the Runtime state machine is transitioned to the QUIT state.

During bootstrapping, you can choose to start the program in developer mode, or do so and also boot into the application directly, skipping the built in splash screen feature.
[01]
Here is a visualization of the pattern:

    ```

    system = System()
    runtime = Runtime(system)
    runtime.run()

    ```
This is where the program begins. 

# System:

We will start our explanation and exploration of the `core/engine` directory by discussing the entrypoints of the system System and Runtime.

System is the framework's service container. It initializes the framework's core services and exposes them through a single object available throughout the application. Let's go over those services that it sets up, one by one, and discuss their functionality and purpose.

To begin I will not elaborate on the hierchical state machine system. That is explained in detail below this section. However to begin, system sets up:

WIP, wrapping all python default modules onto the system object as needed.

Math:

        ```system.math = python math```

Random:
        
        ```system.random = python random```

Setting up globally accessible state machines

State:

        ```system.runtime_state```

A standalone state machine used by Runtime to manage what core state to route to. They are as follows:
RUNTIME_STATE.SPLASH - intermediate behavior as I remove this as a core assumption once I include a splash editor in the editor.
RUNTIME_STATE.APPLICATION - What happens during this state is controlled by you, the developer
RUNTIME_STATE.QUIT - Invoking this state closes the program gracefully.

Acceseed and transformed via valid transitions by:
           
         ```states = [SPLASH,APPLICATION,QUIT]```

checking state:     

        ```system.runtime_state.is_state(RUNTIME_STATE.[states])```

setting state:

        ```system.runtime_state.set_state(RUNTIME_STATE.[states])```

Note: you will rarely be using this state machine to manage your application. You really shouldn't ever touch this one



        ```system.overlay_state```

DEBUG_OVERLAY_STATE.ON - The state that causes the debug overlay to be shown on top of everything.
DEBUG_OVERLAY_STATE.OFF - The state that causes the debug overlay to cease displaying
A standalone state machine used by the Runtime to dictate when to display the debug overlay.

- Press F9 to toggle the debug overlay. This shows the current track, framerate, networking information, and whatever you pass to ```system.app_inspector``` (see below) and the state tree for all active states, including RUNTIME_STATE

Acceseed and transformed via valid transitions by:
           
        ```states = [ON,OFF]```

checking state:     

        ```system.overlay_state.is_state(DEBUG_OVERLAY_STATE.[states])```

setting state:

        ```system.overlay_state.set_state(DEBUG_OVERLAY_STATE.[states])```



        ```system.control_state```

A standalone state machine for controlling a specially privilaged control mode in the program: DEVELOPER_MODE.

Developer mode is triggered by pressing F2 on your keyboard. This can be used for controlling developer features in your application. When it is enabled, you can turn on advanced features to help you. By default, when it is active, a red banner is shown in the bottom right hand corner of the Debug Overlay saying ```WARNING: DEVELOPER MODE IS ENABLED```

Acceseed and transformed via valid transitions by:
        
        ```states = [ON,OFF]```

checking state:     

        ```system.overlay_state.is_state(DEBUG_OVERLAY_STATE.[states])```

setting state:

        ```system.overlay_state.set_state(DEBUG_OVERLAY_STATE.[states])```



        ```system.state_monitor_state```
        
A standalone state machine for managing the state of the state monitor in the top right hand corner of the debug overlay

When the debug overlay is active:

- F8 + 1: Show all global active SYSTEM states (system level state machines like fetching data, sound system states, etc...)
- F8 + 2: Show all global active RUNTIME states (all runtime level state machines such as RUNTIME_STATE)
- F8 + 3: Show all global active APPLICATION states (All application level state machines created by you)
- F8 + 4: Show all global active states

These are all for observing the active state of all state machines during runtime. The hierarchy for state machines is flexible enough, that you don't absolutely have to use them for you programs, but they do act as a core part of the runtime. They are powerful and useful for definining time-sensitive functionality

        A- F8 + 1: Show all global active SYSTEM states (system level state machines like fetching data, sound system states, etc...)
- F8 + 2: Show all global active RUNTIME states (all runtime level state machines such as RUNTIME_STATE)
- F8 + 3: Show all global active APPLICATION states (All application level state machines created by you)
- F8 + 4: Show all global active states

These are all for observing the active state of all state machines during runtime. The hierarchy for state machines is flexible enough, that you don't absolutely have to use them for you programs, but they do act as a core part of the runtime. They are powerful and useful for definining time-sensitive functionalitycceseed and transformed via valid transitions by:
           
        ```states = [RUNTIME,SYSTEM,APPLICATION,ALL]```

checking state:     

        ```system.state_monitor_state.is_state(MONITOR_STATE.[states])```

setting state:

        ```system.state_monitor_state.set_state(MONITOR_STATE.[states])```

This is another on you probably will likely never want to touch directly, however you will find it useful for debugging your applications provided you use the state machine pattern

Setting up the Time object:

    ```system.time = Time()```

    This contains helper functions for delta time and other time related operations

Save Schema:
    
    ```system.save_schema = {}```

The save schema pulls from core/application/save_schema.py where you can set values and data types to be saved using the built in serializeation system set up below (see Persistence). This is useful for creating game saves in a safe, serialized format that can easily be reloaded and modified at any time.

System Monitor:

    ```system.system_monitor = {}```

System monitor is a dictionary whose contents are passed to the Debug Overlay to display system level diagnostics. This will not commonly be used by you.

Persistence:

    ```system.persistence = Persistence(System)```

This, as the name implies is the persistence layer. It is the first core service instantiated and handles saving constant files, environment variable files, and the framework's custom save format for game data/application data. It also supports loading these files, as well as loading UI files for the UI framework (core/ui) to interpret and determine active UIs. 

This system will be explored later, when we talk about saving data, and using the editor with the framework.

We then assign the save_schema to the Persistence object to let that system take over full control of that file.

    ```system.persistence.save.save_schema = self.save_schema```

Updating:

    ```system.update = Update()```

The next module set up is the Update Module. This provides an easy API for checking for updates to your custom game client via API urls set in ```config.py``` within the root directory of the framework. You can set where it checks for updates, when it downloads them (usually I have it set so a user can just click an update button in their client, but UI is up to you). This is part of the larger build and distribution system which we will go over later.

Networking:
    
    ```system.network = Network()```

The Network module handles boilerplate authentication actions and depends on the endpoints set up in core/engine/network/system_endpoints.py, which is a config file that pulls your custom API key and version data from your ```config.py``` file. This allows you to set your custom versioning and plug it into the framework. You shouldn't have to directly touch ```system_endpoints.py``` and if you need custom endpoints, set them in the ```config.py``` file and call them from core/application/network/endpoints.py

User:

    ```system.user = User()```

This is a facade wrapper to handle basic user functions. This sets everything for your users, so if you want to manage networking with auth, you can use the system.user module to manage the username, and any other getters and setters you set in core/engine/user.py

Auth:

    ```system.auth = Authentication()``` 

This is another module from core/network, and it handles basic username/password authentication, with direct built in support for handling server assigned client app passwords and client IDs as well. This is good for managing clients and their versions. Full documentation on this will be part of the NETCODE section of this readme, and will walk you through getting set up connecting your custom application to a remote database utilizing the endpoint system.

Window:

    ```system.window = Window(system)```

This instantiates the Window module, that wraps all of Pygame-CE's window instantiation functions as well as Pygame's draw functions into a neat API that works with the entire system, keeping you from having to use PyGame at all during your development time. This will be a core module you use all the time for all your rendering. I will provide all methods of this class as well as the other core service modules showing how to use their methods.

Sound:

    ```system.sound = AudioEngine(system)```

The naming for this isn't great at the moment, but essentially, the AudioEngine module, completely wraps all of PyGame-CE's audio functions into a neat wrapper you'll likely never spend much time thinking about. Ultimately it allows for volume controls of sound effects, and music, which are handled separately. (sfx_volume_up/down for sfx, volume_up/down for music). The big parts you'll need to use in your games/applications are system.sound.play_music(song="optional title for a specific track"). If you pass a song, it will play on repeat, otherwise,  if left empty, the music system randomly plays files in the assets/sounds/music directory.

You can also call system.sound.play_sfx(effect_name). This works just like the music system, except for there is no repetition and the files are not dynamically loaded for random play. This keeps it simple for playing a sound effect at a specific time, like when you click a button on the UI, or if you want a sound effect to play in your game during a specific state, this system lets you do that with ease.

Input:

    ```system.input = InputManager(system)```

Arguably as important as anything else, any application you make will generally require user input. There is a whole event system, and self-contained, extensible command system baked into it. It wraps all of pygame's event handling in a single neat place, with event checking for all sorts of events including but not limited to: mouse_movement, keypresses, keydown events, window resizing events, etc...

This will be heavily elaborated on, but generally you'll use every single one of these commands within your handle_event(event,command) method from the Application class, and whatever you establish beneath it.

App Inspector:

    ```system.app_inspector = {}```

Like the system monitor, data passed to this dictionary is immediately displayed on the Debug Overlay automatically. This is what you'll use if you want to display something like your player's coordinates, or other debugging info for your specific application directly onto the bulit in F9 debug overlay. Very useful observability tool. You can do so by doing this:

    ```system.app_inspector["your_key"] = "Whatever you want to store"```

It will show on the Debug Overlay on the left hand side in order of when you add each item as:

    """your_key: Whatever you want to store"""


Application:

    ```system.application = None```

The `system.application` variable contains, when your application is running, the actual interface you interact with when building your application. You'll access this from your `Application` class, located in `core/application/application.py`, you'll access it via `Application.distant_realms`. However, that the representation of the `system.application` variable. When your application is initialized, the `System` runs its `System.initialize_application()` method. The `DistantRealms` class is assigned to ```system.application```. This makes your application entirely hot reloadable. 

That covers the core modules set up on the System object. Calling methods on these modules will allow you full control of your application from the bottom up. With the Runtime class handling the core event loop/routing, you will never write a ```while True``` loop again when creating an application. Below we will continue with explaining how Runtime works, and following that, I will start adding the documentation for the Window, Sound, and Input systems, and I will begin discussing how to best start your project, be it a game, inventory management desktop application, or anything else!


# System methods

Before moving onto the next core system, I'd like to document the few methods that exist on the System class, why they are there, and how you can use them.

    ```system.control_state_toggle()```

The control state toggle is as it sounds, it toggles the Developer Mode on and off when called. In order to toggle it during runtime, as mentioned earlier in the System initialization overview, you press the F2 key at any time during the runtime.

    ```system.overlay_state_toggle()```

The overlay state toggle is as it sounds, it toggles the Debug Overlay on and off when called. This is set up in the system to use the F9 command, but this can be overwritten using the engine's built in command system by calling: ```system.input.CommandModule.sequences["debug"] = [youroverwritecommand]```

Although, I don't recommend overwriting the commands that are already in there. A full list can be found at the top of the Input system documentation below.

    ```system.quit()```

Again something else self-explanitory. This method sets the RUNTIME_STATE to RUNTIME_STATE.QUIT, and closes the program gracefully. This can be accessed from anywhere in the program.

    ```system.initialize_application()```

This method bootstraps the application by instantiating an DistantRealms from core/engine/distant_realms.py (soon to be renamed DistantRealms and be included in core/engine). It begins by importing the DistantRealms, allowing for hot reloading without a lot of effort, and then sets the RUNTIME_STATE to RUNTIME_STATE.APPLICATION, sets the MONITOR_STATE to MONITOR_STATE.APPLICATION so the debug overlay automatically shows the running APPLICATION states without all the other system state machines to worry about. By default it only includes APP_STATE.RUNNING, but as you add state machines, it includes them as well. How to do so is documented below under the State Machine section.

    ```system.clean_up_states(states=[])```

This is the only method on the system service that contains a single parameter. You pass a list with the states of active state machines like so:

Pretend we have an Application class that runs, but it has a state machine it uses to manage itself
[02]
    ```
        from core.state.ApplicationLayer.MyApp.state import MY_APP_STATE
        from core.state.ApplicationLayer.MyApp.statemanager import MyAppStateManager

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system

                self.state =  MyAppStateManager()

            ...

            def clean_up_states(self):
                self.system.clean_up_states([self.state.state])

            ...
    ```

Notice the pattern that keeps getting introduced. Cleaning up states ultimately just clears what exists in the state monitor's state lists. If your state machine is in one of those lists, this is how you clear it so it doesn't show on the Debug Overlay, when that state machine's parent object (Application) in this case, is not active.

This is not a functional system. This is purely for observability. State machines manage themselves otherwise when it comes to state transitions.

However with that out of the way, we can move onto the next system overview.

# Runtime

The next portion of the core system located in core/engine that I want to talk about before moving into the usage of each submodule of the services container is the Runtime class.

This class establishes the runtime as its name would suggest, and it is the core part of the system that routes what is currently happening to the application. It has its own state machine that was documented above ```RUNTIME_STATE```. This class contains 2 methods to handle all event routing: ```handle_event``` and ```run```

Handle event dispatches events to the input system dependent on the ```RUNTIME_STATE```. This is handled in the whlie loop in ```run()```. 

Event order is extermely self-explanitory, so instead of painstakingly walking you through the architecture, you can see for yourself

    ```
    def run(self):
        while not self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
            self.system.window.fill(black)
            self.handle_events()

            if self.system.runtime_state.is_state(RUNTIME_STATE.SPLASH):
                self.loading.update()
                self.loading.draw()

            elif self.system.runtime_state.is_state(RUNTIME_STATE.APPLICATION):
                if self.system.application is not None:
                    self.system.application.update()
                    self.system.application.draw()
                else:
                    pass
            elif self.system.runtime_state.is_state(RUNTIME_STATE.QUIT):
                self.system.window.quit()
                sys.exit()
            if self.system.overlay_state.is_state(DEBUG_OVERLAY_STATE.ON):
                self.debug_overlay.update()
                self.debug_overlay.draw()
            
            if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                pass

            if self.loading.state.is_state(BOOT_SPLASH_STATE.NONE):
                self.system.clean_up_states([self.loading.state.state])
            
            self.system.time.timer()
            self.system.window.update()
    ```

It's really, very straightforward. First it fills the screen with a fixed, solid color, establishes the event listener, and then immediately starts checking the RUNTIME_STATE. As you can see, the state machine pattern discussed briefly in the System overview. This is a consistent pattern you'll see everywhere, and you'll even learn to use it yourself for your own applications later on in this documentation!

Notice that Developer Mode, and the Debug Overlay are considered first class systems and can be used during any point in the application. This is useful for obvious reasons, such as live introspection into current application state

# MAIN.PY/KERNEL

Okay so, so far you've seen the System services container and the Runtime loop, and you should have a decent understanding of how they work in tandem to provide you easy to use services to start your application. 

The last thing I'd like to go over in regards to the System/Runtime relationship is how they are instantiated, so you can have a better understanding of the bootstrapping and initialization of the application. This section is not at all important for making games, but is good to understand anyway. It's something I wish was documented more clearly in other frameworks.

So since i've already explained the basic initialization at the top of this file, i'm going to show the main.py file in the root directory by itself since it should be self-explanitory at this point:

    ```
        import argparse
        from core.guts.runtime import Runtime
        from core.guts.system import System
        from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

        def main():
            parser = argparse.ArgumentParser(description="Game Startup")
            
            parser.add_argument('--dev', action='store_true', help="Enable developer mode")
            parser.add_argument('--devg', action='store_true', help="Enables developer mode and opens the game in Endless mode, skipping the menu")

            args = parser.parse_args()

            system = System()
            runtime = Runtime(system)

            if args.dev:
                system.control_state.set_state(DEVELOPER_MODE.ON)
            elif args.devg:
                system.control_state.set_state(DEVELOPER_MODE.ON)
                system.initialize_application()
            runtime.run()

        if __name__ == "__main__":
            main()

    ```

Essentially structured like any C application you'll see, and frankly how I think every main file should look. It does very little work. It instantiates both the System and Runtime and then runs the software, and depending on what flags you pass, you get access to different features. As explained earlier you can start the program in developer mode or both developer mode and skip the splash screen. The same thing happens when you start the executable, but pyinstaller takes care of the initialization of this file.

# system.window

Okay, now we begin to get into the meat and potatoes of the system that makes it so easy to make working applications. We're going to begin this section the same way I began System. With showing the instantiation variables that can be accessed on the window.

Though note, most of the time you will not be accessing most the of the members of Window that are not methods. The properties are largely setup.

    ```
        Window.system - uses the System services container to access system wide utilities
        Window.default_width - default window width
        Window.default_height - default window height
        Window.color - defines the default fill color of the window. This is overwritten by the runtime and is largely redundant
        Window.width - current window width set to None by default
        Window.height - current window height set to None by default
        Window.fps - sets the default FPS cap
        Window.fullscreen - False by default
        Window.rect - used to create pygame.Rects for use in your application. Replaceable backend
    ```

You'll likely find yourself never touching these properties, but it's good to know what the Window sets up at initialization

Below we'll show you the methods you can call to draw primitives like rectangles, circles, lines and polygons, as well as images onto the window. I will not be including the conceptually private methods, only the public interfaces.

    ```Window.mask(surface)```

Returns ```pygame.mask.from_surface(surface)```

Allows you to create masks easily around surfaces, so you don't have to use rects to determine collision. A nice abstraction provided by pygame for pixel perfect collision

    ```Window.transform_scale(original_surface,new_surface_w, new_surface_h)```

Transforms a surface's width/height parameters while maintaining scale. 
Returns ```pygame.transform.scale(original_surface,(new_surface_w,new_surface_h))```

    ```Window.transform_smoothscale(original_surface,new_width,new_height)```

Much like the above method, this returns ```pygame.transform.smoothscale(original_surface,(new_width,new_height))```

    ```Window.get_width()```

Returns the width of the window in pixels

    ```Window.get_height()```

Returns the height of the window in pixels

    ```Window.get_size()```

Returns the window size as a tuple (width,height)

    ```Window.fill(color,alpha=True/False/None)```

Fills the window with a set color, a tuple of 3 positions for a solid color (R,G,B):
    
    ```system.window.fill((R,G,B))```
    
Or if Alpha (0-255) is set to true for the surface, you can pass:

    ```system.window.fill((R,G,B), A)```

Simple method, but powerful and is great for testing different application states.

    ```Window.draw_overlay(color,alpha)```

A simple method for drawing a transparent overlay. Good for simple lighting. This method creates a new surface, purely for displaying a transparent, or opaque overlay.

Usage is straightforward and mirrors Window.fill() although this feature may soon be deprecated:

    ```overlay = system.window.draw_overlay((R,G,B), A)```

Currently it can be used by blitting it with a custom rect, you could do something like ```overlay_rect = overlay.get_rect()``` and then blit it via the included blit functionality below.

    ```Window.blit(surface, destination, area=None)```

It takes a surface (we could use overlay from for instance), a destination, you can pass something like overlay_rect here, and an area, takes a custom area of the surface you're drawing to, to specify where the blit should happen. Although, this is a compatibility point for pygame, and I personally have not made much use of areas as make_surface allows you to create as many arbitrary surfaces as you want on the window. Here is an example of how you would use this in your application's draw method using our ```overlay``` example above:
[03]
Here is some example usage:

    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system
                self.overlay = self.system.window.draw_overlay((255,255,255),120)
                self.overlay_rect = self.overlay.get_rect()

            ...
            
            def draw(self):
                self.system.window.blit(self.overlay,self.overlay_rect)
                """your other drawing logic"""
            ...
    ```

As you can see, this follows pygame's conventions with optionally replacing pygame in the future being an option i'm exploring.

    ```Window.load_image(file_path)```

Pretty self-explanatory, you can dynamically load images from your assets. This actually returns a copy of the surface it is rendered to on the backend, so it calls ```pygame.image.load(file_path)```, runs ```convert_alpha``` on it for preserving transparency, creates a copy, and returns the copy.
[04]
Here is some example usage:

    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system
                self.image = self.system.window.load_image('path/to/my/file' or absolute path)
                self.image_rect = self.image.get_rect()         

            ...

            def draw(self):
                self.system.window.blit(self.image,self.image_rect)
            ...
    ```
Like other methods in this API, its usage is incredibly straightforward, and if you've used pygame before, this will be very familiar.

    ```Window.draw_line(point_a,point_b,color=(R,G,B),width=1)```

This method draws a line from the defined ```point_a``` to defined ```point_b``` with the assigned color tuple, and a pixel width that is totally optional by default.
[05]
Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 
            ...

            def draw(self):
                self.surface.fill(black)
                self.system.window.draw_line((24,44), (208,48),blue,width=2)
            ...
    ```

Again, just like pygame, but with the comfort of knowing most of the backend work is handled for you and that this is all you have to write to make that a reality.

    ```Window.draw_polygon(surface, color=(R,G,B), points=[])```

This method draws an arbitrary polygon and wraps ```pygame.draw.polygon``` though it does not return it and draws right away without blitting just like draw_line.
[06]
Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

                ww = self.system.window.get_width()
                wh = self.system.window.get_height()

                self.surface = self.system.window.make_surface(100,100,False)
                self.rect = self.surface.get_rect(center=(ww/2,wh/2))
            ...

            def draw(self):
                self.surface.fill(black)
                self.system.window.draw_polygon(self.surface,blue,points=[(201,50),(250,50),(225,100)]) #triangle
            ...
    ```

Much like draw_line, this is very easy to set up and use

    ```Window.draw_rect(surface, color, rect, width=0, border_radius=None, object=None)```

This seems like it does a lot more, but really it's quite simple like the previous two methods.

For a bit of elaborating the difference you see here should be obvious, but here, we present with a Surface, a Color, a Rect (x,y,w,h), a border width, a border radius value for rounded corners, and the object it exists on ```object="Player"``` for example. This is for debugging. If your values are incorrect an error will be outputted to core/logs/error.log, hence adding the object property is useful for debugging but optional.
[07]
Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

                ww = self.system.window.get_width()
                wh = self.system.window.get_height()

                self.surface = self.system.window.make_surface(100,100,False)
                self.rect = self.surface.get_rect(center=(ww/2,wh/2))
            ...

            def draw(self):
                self.surface.fill(black)
                self.system.window.draw_rect(self.surface,blue,(50,24,100,100),border_radius=2,object="Application")
            ...
    ```

Again simple to use, but has some debugging features not included in pygame.draw.rect despite the fact that's all that it really is.

    ```Window.draw_circle(surface,color,center,radius,object=None)```

Again the draw circle takes an object for outputting errors if there are errors. Like draw_rect, and draw_polygon, it takes a surface to draw to, a color in an RGB tuple, the center point of the circle, and the radius of the circle, and finally an option to pass an Object for debugging. 
[08]
Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

                ww = self.system.window.get_width()
                wh = self.system.window.get_height()

                self.surface = self.system.window.make_surface(100,100,False)
                self.rect = self.surface.get_rect(center=(ww/2,wh/2))
            ...

            def draw(self):
                self.surface.fill(black)
                self.system.window.draw_circle(self.surface,blue,(50,50),15,object="Application")
            ...
    ```

If you can use the other primitives, this should be straightforward as well.

# system.sound

For this next trick, you're going to need to open your ears, or perhaps have them sewn shut should your sound effects make the Brown Note.

In all seriousness, ```system.sound``` is pretty straightforward as a subsystem as you really only have to remember a few different methods:

We're going to begin with the constructor of AudioEngine as we did for System and Window. This will give you an idea of how the audio system is initialized without going into useless detail about the code itself or exposing every member:

    ```

        AudioEngine.system - the Audio Engine takes the system container like most subsystems in this framework
        default_volume is set to 0.3/1
        AudioEngine.interface_sfx_state - Sets up a state manager for UI sound effects (button clicks, hovers, etc...)
        AudioEngine.app_sfx_state - sets up a state manager for application sfx toggle (game sfx for example)
        AudioEngine.music_state - State manager for determining if music is enabled/disabled
        AudioEngine.music_tracks - a dictionary that receives all the files in assets/sounds/music/ and makes them callable by title.
        AudioEngine.sound_effects - a dictionary that like AudioEngine.music_tracks does the same thing with files in assets/sounds/sfx
        AudioEngine.volume - Music volume loaded from disk
        AudioEngine.sfx_volume - SFX volume loaded from disk
        AudioEngine.current_track - stores a string of the title of the current track being played.

    ```

Now for the methods themselves. This is how you'll interact with the audio system. It's fairly straightforward and I'll show you how:

    ```
        AudioEngine.play_music(str(track) = None)
    ```

Allows you to play a given music file by track name (everything before your file extension) if you pass a track to it. Otherwise if you don't pass a track to it, it'll randomly play music files from the assets/sounds/music directory until you disable the music. You can also pass "stop" to it and it will stop all music.
[09]
Here is some example usage:

    ```
        from core.state.ApplicationLayer.state import APP_STATE
        from core.state.ApplicationLayer.statemanager import AppStateManager

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 
                self.state = AppStateManager()

                self.system.sound.play_music()

            def update(self):
                if self.state.is_state(APP_STATE.FROZEN):
                    self.system.sound.play_music("stop")
                
            def start_app(self):
                self.system.sound.play_music("My Music Track")
            ...
    ```
All the other parts of the ```system.sound``` API work just like this for the most part, although this particular method has more options than others

    ```system.sound.play_sfx(sfx_name)```

This does exactly what you would expect it to. It plays a given sound effect in assets/sounds/sfx. That's all it does.
[10]
Here is some example usage:

    ```
        from core.state.ApplicationLayer.MyGame.Powerup.state import POWERUP_STATE
        from core.state.ApplicationLayer.MyGame.Powerup.statemanager import PowerUpStateManager

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 
                self.power_up_state = PowerUpStateManager()

            def update(self):
                if self.power_up_state.is_state(POWERUP_STATE.POWERUPONE):
                    self.system.sound.play_sfx("powerup1")
            ...
    ```

Even easier with that. 

    ```system.sound.play_ui_sfx(sfx_name)```

The same goes for playing UI SFX, which you likely won't need to worry about as UI sfx, are mostly routed by the framework, but you're welcom to add your own. 
[11]
Here is some example usage:

    ```
        from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE
        from core.state.RuntimeLayer.UI.Button.statemanager import ButtonStateManager

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 
                self.button_state = ButtonStateManager()

            def update(self):
                if self.button_state.is_state(BUTTON_STATE.HOVER):
                    self.system.sound.play_ui_sfx("buttonhover")
            ...
    ```

For ```AudioEngine.volume_up()```, ```AudioEngine.volume_down()```, ```AudioEngine.sfx_volume_up()```, and ```AudioEngine.sfx_volume_down()```,
I recommend following a similar pattern though you'll likely want to tie these into button actions to be triggered at some point. In fact, there is a default settings menu system included with this framework that has volume controls in it. I will however leave this section out as it will map more cleanly to the UI framework usage, for things like the Action Register.

Overall, that wraps up most of what you'll need to process simple audio with the framework. This system will likely greatly improve later on.

# system.input

To begin with the input system, this may see some large changes over the next 6-8 months, however, this is how to use it in its current form. We're going to start, like the previous APIs by documenting the InputManager class' constructor.

    ```
        InputManager.system - Like most other classes, the InputManager class also takes a System in its constructor
        InputManager.CommandModule - an object of the CommandModule class, we'll continue after InputManager with this class
        InputManager.keys - an object of the Keys class, this contains a method for every kind of key press. It wraps pygame's key constants.
        InputManager.game_controls - the last relic of game mentions in the program. I really think with the pattern I have that having a Controls class specifically for managing game input. This allows you to allow custom key-mapping per user input. It's a feature that I'm on the fence leaving in since it's really the last muddy line between application concerns and the engine itself in the codebase.
    ```

So yeah, this system is bloated and full of terrible ideas, but the things that are good, are useful, and that's largely in the methods as well as the ```system.input.keys.*_key()``` API, and the ```system.input.CommandModule``` API. 

Before starting the InputManager's methods, I'd first like to exlain how it's used. Normally with Pygame, or GLFW, or even SDL, you're going to see a similar event loop. So I decided that all input needs to take place in a class' handle_event() method, and the standard for the API is this:
[12]
Here is some example usage:

    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

            def handle_event(self,event,command=None):
                if event.type == self.system.input.keydown():
                    if event.key == self.system.input.keys.up_arrow_key():
                        # do up arrow key stuff
            ...
    ```

As you can see the API is extremely straightforward for checking keypresses. All event types implemented are part of the InputManager class and are methods that return pygame events. So if you've used pygame, you'll be at a major advantage using this framework. In the above script, we don't need to do a for loop or a while loop. You just check the event argument. This should be passed down to all ```handle_event``` methods. As you start in the application class, its ```handle_event``` method is called by default. A full List of the keys will be inlcuded at the bottom of the section on #system.input.

I also want to go over the Command Module. Another very straight forward tool that can also be used in conjunction for keys. Below are the built in sequences you can use globally. Commands you create are local to where you create them and only exist during the RUNTIME_STATE.APPLICATION, and if deeper, then wherever you decide to put them.

    ```
        CommandModule.sequences = {
            "debug": [self.keys.F9_key()],
            "developer": [self.keys.F2_key()],
            "monitor_system_states": [self.keys.F8_key(),self.keys.one_key()],
            "monitor_runtime_states": [self.keys.F8_key(),self.keys.two_key()],
            "monitor_application_states": [self.keys.F8_key(),self.keys.three_key()],
            "monitor_all_states": [self.keys.F8_key(),self.keys.four_key()],
            "raise_opacity": [self.keys.F8_key(),self.keys.five_key()],
            "lower_opacity": [self.keys.F8_key(),self.keys.six_key()],
            "reload_ui": [self.keys.F1_key(),self.keys.one_key()],
            "reload_application": [self.keys.F1_key(),self.keys.two_key()],
            "reload_menu_editor": [self.keys.F1_key(),self.keys.three_key()],
            "reload_form_editor": [self.keys.F1_key(),self.keys.four_key()]
        }
    ```

[13]
Here is an example of how to create and use your own commands. The implementation is identical to core/engine/runtime.py, but runtime.py actually creates the command variable. You just get to check it for a given command. The interval for pressed key combos for commands is 5000ms. You can set whatever command you want, but it must not conflict with the above sequences or you'll overwrite key functionality. Here we go:

    ```
        from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

                self.system.input.CommandModule["my_command"] = [self.system.input.keys.F7_key()]

            def handle_event(self,event,command=None):
                if self.system.control_state.is_state(DEVELOPER_MODE.ON):
                    if command == "my_command":
                        # Do some developer mode stuff
            ...
    ```

In example [13], I actually use another system in the framework to demonstrate a nice use of Developer Mode. This is the system.control_state state machine. We check for if developer mode is on (again, you can do this by pressing F2 or starting the program with the --dev or --devg flags). If it is, we check if the command has occurred. If it has, we do the stuff you assign in the command.

Now that we're somewhat familiar with the way the input system works with its keys and commands, and some basic conditions, let's show the important event methods on the InputManager class. These are all used identically to how we're using ```system.input.keydown()``` on example [12].

Here are the event methods on the InputManager class called with system.input.(event())

    ```system.input.video_resize_event()```

This method returns a pygame.VIDEORESIZE event. You can use this in your ```scale``` method. The ```scale``` method on the ```Application``` class, where you start your work, is already automatically called, so feel free to use it. You can also just use this method straight away.

    ```system.input.get_mouse_pos()```

This method returns the mouse position in screen coordinates as a tuple (EX: (24,42))

    ```system.input.mouse_button_down()```

This method returns a pygame.MOUSEBUTTONDOWN event. It returns a boolean and you can then check ```event.button``` just like on the below example. 

1 is for left click; 
2 is for middle click; 
3 is for right click;

[14]
    ```
        from core.util.colors import *

        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

                ww = self.system.window.get_width()
                wh = self.system.window.get_height()

                self.surface = self.system.make_surface(40,40)
                self.rect = self.surface.get_rect(center=(ww/2,wh/3)) # Will always return a pygame-like rect. rect.collidepoint() will always work
                self.surface.fill(red)

            def handle_event(self,event,command=None):
                mouse_pos = self.system.input.get_mouse_pos()
 
                if event.type == self.system.input.mouse_button_down():
                    if self.rect.collidepoint(mouse_pos):
                        # do your action that happens when you click the rectangle

            ...
    ```
Now you know not only how to use the input system, but one of the ways to make a basic clickable object! Yay for you!

    
    ```system.input.mouse_button_down()```

This method returns a `pygame.MOUSEBUTTONDOWN` event.

    ```system.input.mouse_motion(self)```

This method returns a `pygame.MOUSEMOTION` event

    ```system.input.get_mouse_pos()```

This method returns a `pygame.mouse.get_pos()` which is just a tuple containing (x,y) coordinates

    ```system.input.keydown()```

This method returns a `pygame.KEYDOWN` event.

    ```system.input.mouse_scroll_event()```

This method returns a `pygame.MOUSEWHEEL` event. Populates `event.y` which is a 1 or a -1. For example:
[15]

    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

            def handle_event(self, event):
                if event.type == self.system.input.mouse_scroll_event():
                    if event.y == 1:
                        # mouse scroll up event
                    else:
                        # mouse scroll down event
        ...
    ``` 

As you can see it's easy enough to do. Eventually i'll provide some basic offset logic for making proper scroll windows. However currently this is mostly used by the ScrollableText widget, which is a configurable box for displaying text.

    ```system.input.get_pressed_keys()```

This method returns ```pygame.key.get_pressed()```. returns a list of `pygame.K_[keys]` currently pressed. This is something that the CommandModule uses, but you can also get it for your games. Say if you wanted to make a character go diagonally on the screen by pressing W and D, you could do that with that method. Just check for if they are equal to `system.input.keys.keyname_key()` rather than using pygame's raw functionality. This will ensure your applications stay compatible with future versions of the framework which may or may not include pygame by default. I will obey the same assumptions if you do.

    ```system.input.window_focus_gained()```

This method returns `pygame.WINDOWFOCUSGAINED`, which if you check it against event.type like in examples [12], [13], [14], and [15], you can do what you'd like with the outcome of `system.input.window_focus_gained()`

    ```system.input.window_focus_lost()```

This method returns `pygame.WINDOWFOCUSLOST` which is the opposite of the previous method. As in the same examples: [12], [13], [14], and [15], you can do what you like when the focus is lost. I recommend pausing your game in that event, if you're making a game.

And that concludes the methods that you need to make games and applications with ```DistantRealms.system.input```

Before we conclude the system.input section, I'd like to leave this key mapping here so you know how to access every key:

The ```Keys``` class provides backend-independent access to keyboard keys. These can all be accessed like in example [13] by calling ```system.input.keys.a_key()``` for every method listed here:

### Alphabetic Keys

| Function  | Key |
| --------- | --- |
| `a_key()` | A   |
| `b_key()` | B   |
| `c_key()` | C   |
| `d_key()` | D   |
| `e_key()` | E   |
| `f_key()` | F   |
| `g_key()` | G   |
| `h_key()` | H   |
| `i_key()` | I   |
| `j_key()` | J   |
| `k_key()` | K   |
| `l_key()` | L   |
| `m_key()` | M   |
| `n_key()` | N   |
| `o_key()` | O   |
| `p_key()` | P   |
| `q_key()` | Q   |
| `r_key()` | R   |
| `s_key()` | S   |
| `t_key()` | T   |
| `u_key()` | U   |
| `v_key()` | V   |
| `w_key()` | W   |
| `x_key()` | X   |
| `y_key()` | Y   |
| `z_key()` | Z   |

### Number Keys

| Function      | Key |
| ------------- | --- |
| `zero_key()`  | 0   |
| `one_key()`   | 1   |
| `two_key()`   | 2   |
| `three_key()` | 3   |
| `four_key()`  | 4   |
| `five_key()`  | 5   |
| `six_key()`   | 6   |
| `seven_key()` | 7   |
| `eight_key()` | 8   |
| `nine_key()`  | 9   |

### Function Keys

| Function    | Key |
| ----------- | --- |
| `F1_key()`  | F1  |
| `F2_key()`  | F2  |
| `F3_key()`  | F3  |
| `F4_key()`  | F4  |
| `F5_key()`  | F5  |
| `F6_key()`  | F6  |
| `F7_key()`  | F7  |
| `F8_key()`  | F8  |
| `F9_key()`  | F9  |
| `F10_key()` | F10 |
| `F11_key()` | F11 |
| `F12_key()` | F12 |

### Modifier Keys

| Function            | Key                 |
| ------------------- | ------------------- |
| `l_ctrl_key()`      | Left Ctrl           |
| `right_ctrl_key()`  | Right Ctrl          |
| `left_shift_key()`  | Left Shift          |
| `right_shift_key()` | Right Shift         |
| `l_alt_key()`       | Left Alt            |
| `r_alt_key()`       | Right Alt           |
| `l_gui_key()`       | Left GUI / Windows  |
| `r_gui_key()`       | Right GUI / Windows |

### Arrow & Navigation Keys

| Function            | Key         |
| ------------------- | ----------- |
| `up_arrow_key()`    | Up Arrow    |
| `down_arrow_key()`  | Down Arrow  |
| `left_arrow_key()`  | Left Arrow  |
| `right_arrow_key()` | Right Arrow |
| `home_key()`        | Home        |
| `end_key()`         | End         |
| `insert_key()`      | Insert      |
| `delete_key()`      | Delete      |
| `page_up_key()`     | Page Up     |
| `page_down_key()`   | Page Down   |

### Lock & System Keys

| Function             | Key          |
| -------------------- | ------------ |
| `caps_lock_key()`    | Caps Lock    |
| `num_lock_key()`     | Num Lock     |
| `scroll_lock_key()`  | Scroll Lock  |
| `print_screen_key()` | Print Screen |
| `sys_req_key()`      | SysRq        |
| `pause_key()`        | Pause        |
| `break_key()`        | Break        |
| `menu_key()`         | Menu         |
| `help_key()`         | Help         |
| `clear_key()`        | Clear        |

### Control Keys

| Function          | Key       |
| ----------------- | --------- |
| `space_key()`     | Space     |
| `return_key()`    | Return    |
| `enter_key()`     | Enter     |
| `escape_key()`    | Escape    |
| `backspace_key()` | Backspace |
| `tab_key()`       | Tab       |
| `backtick()`      | `         |

> **Note:** `return_key()` and `enter_key()` currently both return `pygame.K_RETURN`.

### Punctuation & Symbol Keys

| Function                  | Key |
| ------------------------- | --- |
| `left_bracket_key()`      | `[` |
| `right_bracket_key()`     | `]` |
| `backslash_key()`         | `\` |
| `semicolon_key()`         | `;` |
| `apostrophe_key()`        | `'` |
| `comma_key()`             | `,` |
| `period_key()`            | `.` |
| `slash_key()`             | `/` |
| `equals_key()`            | `=` |
| `minus_key()`             | `-` |
| `underscore_key()`        | `_` |
| `plus_key()`              | `+` |
| `asterisk_key()`          | `*` |
| `colon_key()`             | `:` |
| `question_mark_key()`     | `?` |
| `less_than_key()`         | `<` |
| `greater_than_key()`      | `>` |
| `ampersand_key()`         | `&` |
| `caret_key()`             | `^` |
| `dollar_key()`            | `$` |
| `percent_key()`           | `%` |
| `hash_key()`              | `#` |
| `at_key()`                | `@` |
| `left_parenthesis_key()`  | `(` |
| `right_parenthesis_key()` | `)` |

### Keypad Keys

| Function                | Key          |
| ----------------------- | ------------ |
| `keypad_0_key()`        | Keypad 0     |
| `keypad_1_key()`        | Keypad 1     |
| `keypad_2_key()`        | Keypad 2     |
| `keypad_3_key()`        | Keypad 3     |
| `keypad_4_key()`        | Keypad 4     |
| `keypad_5_key()`        | Keypad 5     |
| `keypad_6_key()`        | Keypad 6     |
| `keypad_7_key()`        | Keypad 7     |
| `keypad_8_key()`        | Keypad 8     |
| `keypad_9_key()`        | Keypad 9     |
| `keypad_period_key()`   | Keypad .     |
| `keypad_divide_key()`   | Keypad /     |
| `keypad_multiply_key()` | Keypad *     |
| `keypad_minus_key()`    | Keypad -     |
| `keypad_plus_key()`     | Keypad +     |
| `keypad_enter_key()`    | Keypad Enter |
| `keypad_equals_key()`   | Keypad =     |

### Backend Abstraction

The purpose of this class is to prevent the rest of the input system from directly depending on Pygame. For example:

    ```
        if input.is_key_pressed(keys.w_key()):
            player.move_forward()
    ```

The input/control system only needs to know about the `Keys` interface. A different backend can provide its own implementation without requiring the rest of the engine to change.


Happy day, we're done with the grueling input documentation. And I've probably still got a million typos to fix, not to mention the Dunning-Kruger effect taking over my psyche, so half the language in this document could be entirely garbage from count slopula himself. Essentially, if you disagree with my terminology, IDK what to tell you. Bye felisha? Wow that was 2000 and late.

# system.persistence

So for this one, it's a pretty simple object. It controls where UI files are found, and routes save and load functions for files on the disk (unrelated to ui files, those are a special case for now)

So what you need to know about the Persistence class, is that it sets up 2 objects you're going to deal with if you're making games or for some reason need to store data to disk. 

    ```system.persistence.save```

    and

    ```system.persistence.load```

You really only need 2 of the methods on each of these objects. They directly mirror each other for our current purposes, so I'm going to give quick and easy examples:

If you're wanting to save a single value to a single file that you can easily reference (say like a username, or a volume file) you can do:

    ```system.persistence.save.write_constant("name of file", "value to store")```

The same interface is provided for reading said files:

    ```system.persistence.save.read_constant("name of file")```

Notice it doesn't give you the choice where to store it. That is because all saves go to the `ROOTDIR/saves/`. Constants like in this section, are stored in `saves/constants`.

The other way of saving uses my custom save format system. You'll want to use this for things like game saves where you're saving a lot of different data types and you need to preserve the typing. This way, the save schema itself is actually the source of truth for typing. You just pass your values, and load your values. Loading is much simpler since again, the schema knows the type. 

    ```system.persistence.save.write_save(data={})```

It stores in `saves/appdata/app.sav`

In order to save to it you can pass data in like this example:
[16]
Enter your save parameters in `core/application/save_schema.py`:

    ```
        #save_schema.py

        schema = {
            "WORLDSEED": ("seed", int),
            "PLAYERWORLDX": ("player_world_x", float),
            "PLAYERWORLDY": ("player_world_y", float),
            "PLAYERHEALTH": ("player_health, float),
            "PLAYERINVENTORY": ("player_inventory", dict)
        }

    ```

As you can see, it just takes in python types directly as the second value in the tuple
[17]
And here's how you would encode it when saving:

    ```
        def serialize(self,player,world):
            return {
                "player_world_x": player.world_x,
                "player_world_y": player.world_y,
                "seed": world.seed,
                "player_health": player.health,
                "player_inventory": player.inventory # maybe a dict
            }
    ```

And then to load it, it's very simple:
[18]
    ```

        load_data = system.persistence.load.load_save()

        player_data = [load_data["player_world_x"],load_data["player_world_y"],load_data["player_health"],load_data["player_inventory"]]

        def load(load_data):
            if load_data is not None:
            game.player = Player(system,saved_data=player_data)
            game.world.seed = load_data["seed"]
    ```

Currently, there is experimental functionality to pass a file to `save.write_save` or `load.load_save` after the data, but that hasn't been fully tested. If you do so, you structure it like this:

    ```system.persistence.save.write_save(data,filename)```

    and

    ```system.persistence.load.load_save(filename)```

This functionality is coded in, so you can use it, but again, it's experimental and may totally just not work. But it will only have a single source of truth so eventually I'll add a third argument for a different schema. That'd be a second argument on the loading method.

# system.time

Well now, we're going to get to the last core element of the `System`, that you'll need in order to build applications. I'm speaking of course of the `system.time` module

There actually isn't a lot to say about this class, it's relatively small and easy to understand. There are really only 2 methods you'll ever really need to make apps here.

    ```system.time.get_current_time()```

This method returns the current amount of milliseconds since the `System` object was instantiated.

    ```system.time.delta_time()```

This method calculates delta time. Here's how you can use it in your application:
[19]
    ```
        from core.application.MyGameStuff.Player import Player

        class Application:
            def __init__(self,distant_realms):
                self.disant_realms = distant_realms
                self.system = distant_realms.system
                self.player = Player()

            def update(self): 
                dt = self.system.time.delta_time()
                # My player movement 
                speed = 200.0 
                # units per second 
                self.player.position.x += speed * dt
    ```

The important thing to understand here is that `delta_time()` gives you the amount of time that has passed since the previous update. This allows movement and other time-dependent operations to be expressed in terms of real time rather than frames. This is clear if you're trying to start a timer since the application started, in which case you'll do:
[20]
    ```
        class Application:
            def __init__(self,distant_realms):
                self.disant_realms = distant_realms
                self.system = distant_realms.system
                self.life_start_time = self.system.time.get_current_time()

            def update(self): 
                current_time = self.system.time.get_current_time()

                timer = current_time - self.life_start_time
    ```

## Core systems wrapup

Welp I'm sure that by now you're itching to get into making some games. At this point you should be able to draw all kinds of primitives and images to the screen. I hope you are also able to handle the event system for your keypresses and other user interactions, as well as be able to trigger `sound effects` and `music`. You should understand how to use the `system.time` module, and how you should be using methods like `system.time.delta_time()` instead of calculating your own. You should even have a decent picture on how to use the state system from a high level, even though I haven't introduced how they entirely work yet. That will come later, but you should be able to use developer mode to great effect already.

However the next system is a big one, and will probably be at least half the size of all of the previous sections combined. The system I'm referring to of course is the easy to use, widget based UI system.

The UI framework, within the **Distant Realms Framework**, located in `core/ui` consists of several components for composing user interfaces. Currently the primary built in composables are Form and Menu. However, if you understand the UI system, you should be able to create your own composable views. 

Now, I would like to make absolutely clear, that to use this framework to make rich user driven interfaces, you absolutely do not have to directly understand the UI system. Before I get to the UI section, I'm going to do you a favor and point you to a useful little install script, and an overview of the `DistantRealms` service, and its member methods and variables, so that you can get started making UIs for your games and applications without having to compose your own interfaces with code. Following this section, I will be explaining the intricacies of the UI framework itself. Which is what 
the **Distant Realms Editor** is built on.

This is not an instruction manual on how to use the editor. This is an instruction manual on how to install and use the editor with your workflow.

In the section **Project Structure**, I pointed out the `tools/` directory. Well that directory is not here by default, and that is by design. To get started with designing your own menus and input data forms, go ahead and run the following command:
[21]
Linux:

    ```bash install_editor_linux.sh```

Windows with GitBash:                               NOTE: Windows support is only as much as I use Windows. Gitbash is the only tested environment

    ```bash install_editor_windows.sh```

It will ask you after install if you'd like to start the editor immediately after installation. Selecting yes will open the editor. Otherwise, you can start the editor by running:

    ```bash run_editor.sh```

If you're running the editor, and using it, via its GUI, it will automatically create and modify files in `enginepersistence/` in both the `forms/` subdirectory and the `menus/` subdirectory. To use this tool, you do not need to know the details of the UI framework laid out in this document as most of it is entirely automatic. It's a simple WYSIWYG editor, and has a project browser, and a fully featured editor for all widgets within the UI system.

All you really need to know in that case, is how to show UIs, and this can be accessed via the `DistantRealms` object, which is passed to the application in all of the `Application` examples above. For reference her is an example of how to access the DistantRealms object, as it is never supposed to be directly called by you, the developer:
[22]
    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 
    ```

As you can see in the above example of the usable `Application` class located in `core/application/application.py`, the distant_realms object is just a variable we have access to. This is how the entire system is injected into your application.

Most framework level systems use the System object directly, but the `DistantRealms` class provides an extra barrier of interfaces that you can interact with and use. 

The important member variable and methods you need to worry about for the UI system are simple however:

    ```Application.distant_realms.ui_controller.show_ui("name of ui")```

When creating a new project in the **Distant Realms Editor**, a file is created in either `enginepersistence/forms/` or `enginepersistence/menus`. The above method makes it so you don't have to know how any of that works. You just get to display your UI at any given time regardless of what it displays or how it displays it. Below I have included an example of how you might use this:
[23]
    ```
        class Application:
            def __init__(self,distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system 

            def init(self):             # This method is called automatically when you start your program
                self.distant_realms.ui_controller.show_ui("my_main_menu")
    ```

One more thing I'd like to point out is how to actually clear the UI system out of your way so you can show your own things, since the UI system is always on top for its views. This is even simpler than the above method:

    ```Application.distant_realms.ui_controller.clear()```

No fluff, nothing extra to take care of. Just clear the UI.

But you're asking me, how in the world do "I, the developer" control the ui elements and dynamically change them? How do I actually connect to button actions and assign functionality to them? And we're about to explain just how to do those things, as that will complete the minimal amount of information you need to know to become productive with this framework at this point, while not having to understand the intricacies of the UI framework. 

Let's begin with `core/application/action_register.py`. This file is something you'll be editing often. See, when you create a Button with the framework, one of its properities is "Action". This is arbitrary. You can name your actions whatever you want. the important part would be following the pattern in the example below, which is a direct copy of the included `action_register.py` file:
[24]
    ```
        class ActionRegistrar:
            def __init__(self, distant_realms):
                self.distant_realms = distant_realms
                self.system = distant_realms.system
                
            def register(self):
                application = self.distant_realms
                application.actions.register("open_changelog",lambda: application.ui_controller.show_ui("changelog"))
                application.actions.register("open_credits",lambda: application.ui_controller.show_ui("credits"))
                application.actions.register("main_menu", lambda: application.ui_controller.show_ui("main"))
                application.actions.register("test_button", lambda: print("Testing"))
                application.actions.register("quit",self.system.quit)
    ```

As you can see, registering one of your button actions is exceptionally trivial to plug into a function.

One thing you will want to make note of is that this example doesn't show exactly how you'll control your own functionality, as it isn't immediately obvious. We'll be introducing another property of the `DistantRealms` class that we interact with via `ActionRegistrar.distant_realms`:

    ```DistantRealms.application```

This variable contains your `Application` class code. Not to be conflated with `system.application` which contains `DistantRealms`. `DistantRealms.application` is your only concern. Since you're expected to plug all of your custom functionality into this class, it is the central access for all your application's needs. 

Therefore if you want to make a Button that you created as part of a UI view with the **Distant Realms Editor**, you would pass its action like so:
[25]
    ```
        def register(self):
            application = self.distant_realms
            ...
                application.actions.register("my_action", application.application.my_action_method)
            ...
    ```

Or if you're using a method of a class that isn't instantiated yet, but still want the button to activate it, you can use a lambda:
[26]
    ```
        def register(self):
            application = self.distant_realms
            ...
                application.actions.register("my_action", lambda: application.application.my_uninstantiated_class.my_action_method())
            ...
    ```

Or like in example [24] where it shows how to use `ui_controller.show_ui()` as a lambda.

This should be pretty easy to implement from here. You can trigger anything with buttons that you want.

Now that we know how to control button click actions from buttons given to you by the **Distant Realms Editor**, we can begin to go over how to actually manipulate the UI elements dynamically from your program. This will mean we get to learn another method on `DistantRealms.ui_controller`.

    ```Application.distant_realms.ui_controller.get_active_ui()```

This method returns the active UI and interacting with the dictionary it returns. Here is a list of all the possible children you will get per UI dictionary:

## UI Objects

| Object | Type | Description | Key Properties |
|---|---|---|---|
| **Button** | `button` | Interactive button with configurable visual states and an optional action | `id`, `text`, `position`, `font_size`, `action`, `styles` |
| **Label** | `label` | Static text element | `id`, `text`, `position`, `font_size`, `color` |
| **Header** | `header` | Large text element intended for headings | `id`, `text`, `position`, `font_size`, `color` |
| **Query** | `query` | Text-based query/input element | `id`, `text`, `position`, `font_size`, `color` |
| **Scrollable Text** | `scrollable_text` | Text area with scrolling support | `id`, `text`, `position`, `color`, `width`, `height`, `align`, `line_spacing`, `font_size` |
| **Textbox** | `textbox` | User text input field | `id`, `field`, `position`, `dimensions`, `font_size`, `max_chars` |
| **Select** | `select` | Dropdown/selectable option field | `id`, `options`, `selected_option`, `position`, `font_size`, `width`, `height`, `padding`, `field` |

### Button Styles

| Property          | `idle` | `hover` | `press` | `disable` | `focused` |
| ----------------- | -----: | ------: | ------: | --------: | --------: |
| **Background**    | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` |
| **Border**        | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` |
| **Border Width**  | `2` | `3` | `2` | `2` | `3` |
| **Border Radius** | `8` | `8` | `8` | `8` | `8` |
| **Text Color**    | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` | `[RED, GREEN, BLUE]` |
| **Padding**       | `5` | `5` | `5` | `5` | `5` |

That should give you a good picture of all of the possible fields you can edit as part of the UI elements in your active UI. 

Here is an example of how the **Distant Realms Editor** edits any of these dynamically using its volume level display as an example:
[27]
    ```
            ui = self.distant_realms.ui_controller.get_active_ui()

            music_volume = float(self.app_interface.system.sound.volume)
            normal_music_volume = str(int(music_volume * 10))

            sfx_volume = float(self.app_interface.system.sound.sfx_volume)
            normal_sfx_volume = str(int(sfx_volume * 10))

            for child in ui.children:
                if child.id == "music_volume_text":
                    child.text = normal_music_volume
                
                if child.id == "sfx_volume_text":
                    child.text = normal_sfx_volume
    ```

With this we can set any of the properties of any of the elements in the actively shown UI to be anything we want, at any time we want! Nifty isn't it?

NOTE: At some point I may include a sprite loader in the `core/application` directory, however it is not a direct priority of the framework until I've finished the workflow.

# State system

## This section is currently a stub

State System Overview

The core runtime backbone is in core/state, based on basestatemanager.py.

You will often see patterns like:

self.system.app_state.set_state(RUNTIME_STATE.MAIN_MENU)

States are defined as enums. Each statemanager.py defines allowed transitions via a dictionary.

State Manager Concepts

Each state manager inherits from BaseStateManager and requires:

initial_state: starting state (e.g., RUNTIME_STATE.SPLASH)
allowed_transitions: dictionary of valid transitions
log_fn: callback for logging transitions
state_name: string name of the state type
type: one of SYSTEM, RUNTIME, or APPLICATION,

All transitions are logged automatically in logs/.

State Layers

There are three layers:

SYSTEM
RUNTIME
APPLICATION

These are stored globally for debugging visibility only. They are not used to control logic.

Example State Enum
```
from enum import Enum, auto

class RUNTIME_STATE(Enum):
    SPLASH = auto()
    APPLICATION = auto()
    QUIT = auto()
```
Example State Manager
```
from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class StateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            RUNTIME_STATE.SPLASH: [RUNTIME_STATE.APPLICATION, RUNTIME_STATE.QUIT],
            RUNTIME_STATE.APPLICATION: [RUNTIME_STATE.QUIT]
        }

        super().__init__(
            initial_state=RUNTIME_STATE.SPLASH,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="RUNTIME_STATE",
            type="RUNTIME"
        )
```
Example Usage
```
from core.state.GameLayer.state import GAMESTATE
from core.state.GameLayer.statemanager import GameStateManager

class Game:
    def __init__(self, system):
        self.state = GameStateManager()

    def draw(self):
        if self.state.is_state(GAMESTATE.PAUSED):
            self.pause_menu.update()
            self.pause_menu.draw()
        elif self.state.is_state(GAMESTATE.PLAYING):
            pass
```
You can use this pattern anywhere, not just in the draw loop. It is central to the menu and runtime system.

More documentation will be added over time. The next major component to document is the system object.