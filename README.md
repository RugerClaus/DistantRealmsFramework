# Welcome to the Distant Realms Framework for Developing Applications with Python
- An application framework with a working tooling ecosystem, proving support for rendering, audio, input, simple networking as well as a ready bulit WYSIWYG ui editor that outputs to a format the engine can read directly. Below you will learn how to make games and other applications using Distant Realms

- Distant Realms is designed around convenience without lock-in.

- The framework provides high-level systems for common application needs, but those systems are built on straightforward underlying APIs. You can use as much or as little of the framework as your application requires.

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

# About 3rd party dependencies:

Pygame-ce provides the backend for creating a window, drawing, audio, and input, as well as some of its time functions. 
The files that use it are as follows:
    -core/guts/window.py
    -core/guts/audioengine.py
    -core/guts/input/inputmanager.py
    -core/guts/input/keys.py
    -core/guts/time.py
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

Here is a visualization of the pattern:

```

system = System()
runtime = Runtime(system)
runtime.run()

```
This is where the program begins. 

# System:

We will start our explanation and exploration of the core/guts directory (later to be named core/engine) by discussing the entrypoints of the system System and Runtime.

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

The Network module handles boilerplate authentication actions and depends on the endpoints set up in core/guts/network/system_endpoints.py, which is a config file that pulls your custom API key and version data from your ```config.py``` file. This allows you to set your custom versioning and plug it into the framework. You shouldn't have to directly touch ```system_endpoints.py``` and if you need custom endpoints, set them in the ```config.py``` file and call them from core/application/network/endpoints.py

User:

    ```system.user = User()```

This is a facade wrapper to handle basic user functions. This sets everything for your users, so if you want to manage networking with auth, you can use the system.user module to manage the username, and any other getters and setters you set in core/guts/user.py

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

Like the system monitor, data passed to this dictionary is immediately displayed on the Debug Overlay automatically. This is what you'll use if you want to display something like your player's coordinates, or other debugging info for your specific application directly onto the bulit in F9 debug overlay. Very useful observability tool. You can do so by doing this

    ```system.app_inspector["your_key"] = "Whatever you want to store"```

It will show on the Debug Overlay on the left hand side in order of when you add each item as:

    """your_key: Whatever you want to store"""

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

This method bootstraps the application by instantiating an AppInterface from core/application/application_interface.py (soon to be renamed DistantRealms and be included in core/guts). It begins by importing the AppInteface, allowing for hot reloading without a lot of effort, and then sets the RUNTIME_STATE to RUNTIME_STATE.APPLICATION, sets the MONITOR_STATE to MONITOR_STATE.APPLICATION so the debug overlay automatically shows the running APPLICATION states without all the other system state machines to worry about. By default it only includes APP_STATE.RUNNING, but as you add state machines, it includes them as well. How to do so is documented below under the State Machine section.

    ```system.clean_up_states(states=[])```

This is the only method on the system service that contains a single parameter. You pass a list with the states of active state machines like so:

Pretend we have an Application class that runs, but it has a state machine it uses to manage itself

    ```
        from core.state.ApplicationLayer.MyApp.state import MY_APP_STATE
        from core.state.ApplicationLayer.MyApp.statemanager import MyAppStateManager

        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system

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

The next portion of the core system located in core/guts that I want to talk about before moving into the usage of each submodule of the services container is the Runtime class.

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

It's reall, very straightforward. First it fills the screen with a fixed, solid color, establishes the event listener, and then immediately starts checking the RUNTIME_STATE. As you can see, the state machine pattern discussed briefly in the System overview. This is a consistent pattern you'll see everywhere, and you'll even learn to use it yourself for your own applications later on in this documentation!

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

It takes a surface (we could use overlay from our previous example for instance), a destination, you can pass something like overlay_rect here, and an area, takes a custom area of the surface you're drawing to, to specify where the blit should happen. Although, this is a compatibility point for pygame, and I personally have not made much use of areas as make_surface allows you to create as many arbitrary surfaces as you want on the window. Here is an example of how you would use this in your application's draw method using our ```overlay``` example above:

    ```
        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system
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

Here is some example usage:

    ```
        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system
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

Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system 
            ...

            def draw(self):
                self.surface.fill(black)
                self.system.window.draw_line((24,44), (208,48),blue,width=2)
            ...
    ```

Again, just like pygame, but with the comfort of knowing most of the backend work is handled for you and that this is all you have to write to make that a reality.

    ```Window.draw_polygon(surface, color=(R,G,B), points=[])```

This method draws an arbitrary polygon and wraps ```pygame.draw.polygon``` though it does not return it and draws right away without blitting just like draw_line.

Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system 

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

Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system 

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

Here is some example usage:

    ```
        from core.util.colors import *

        class Application:
            def __init__(self,app_interface):
                self.app_interface = app_interface
                self.system = app_interface.system 

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

# Feature Additions

Before adding new features, check the requested_additions file in the root directory. Try implementing one of those ideas first, then submit a pull request.

Developer Mode
Debug Overlay

Press F2 to enter developer mode. This will eventually allow opening a developer console and modifying game variables, including executing Python code.

Work happens in core/application.

State System Overview

The core runtime backbone is in core/state, based on basestatemanager.py.

You will often see patterns like:

self.system.app_state.set_state(RUNTIME_STATE.MAIN_MENU)

States are defined as enums. Each statemanager.py defines allowed transitions via a dictionary.

State Manager Concepts

Each state manager inherits from BaseStateManager and requires:

initial_state: starting state (e.g., RUNTIME_STATE.LOADING)
allowed_transitions: dictionary of valid transitions
log_fn: callback for logging transitions
state_name: string name of the state type
type: one of SYSTEM, APPLICATION, or GAME

All transitions are logged automatically in logs/.

State Layers

There are three layers:

SYSTEM
APPLICATION
GAME

These are stored globally for debugging visibility only. They are not used to control logic.

Example State Enum
```
from enum import Enum, auto

class RUNTIME_STATE(Enum):
    LOADING = auto()
    MAIN_MENU = auto()
    GAME = auto()
    QUIT = auto()
```
Example State Manager
```
from core.state.ApplicationLayer.state import RUNTIME_STATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class StateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            RUNTIME_STATE.LOADING: [RUNTIME_STATE.MAIN_MENU, RUNTIME_STATE.QUIT],
            RUNTIME_STATE.MAIN_MENU: [RUNTIME_STATE.GAME, RUNTIME_STATE.QUIT],
            RUNTIME_STATE.GAME: [RUNTIME_STATE.MAIN_MENU, RUNTIME_STATE.QUIT]
        }

        super().__init__(
            initial_state=RUNTIME_STATE.LOADING,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="RUNTIME_STATE",
            type="APPLICATION"
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