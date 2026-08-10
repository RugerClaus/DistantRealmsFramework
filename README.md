# Welcome to the Distant Realms Framework for Developing Applications with Python
- An application framework with a working tooling ecosystem, proving support for rendering, audio, input, simple networking as well as a ready bulit WYSIWYG ui editor that outputs to a format the engine can read directly. Below you will learn how to become productive at making games and other applications using Distant Realms

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

The system object contains all core services for the engine, as you've likely already read above. Let's go over those services that it sets up, one by one, and discuss their functionality and purpose.

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


        Acceseed and transformed via valid transitions by:
           
            ```states = [RUNTIME,SYSTEM,APPLICATION,ALL]```

            checking state:     

                ```system.state_monitor_state.is_state(STATE_MONITOR_STATE.[states])```

            setting state:

                ```system.state_monitor_state.set_state(STATE_MONITOR_STATE.[states])```


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

    This, as the name implies is the persistence layer

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