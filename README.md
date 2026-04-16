# Welcome to Distant Realms, a top-down survival RPG

## Dependencies

This project has a few dependencies. The only third-party assets are the fonts in `assets/font`.

It uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. See `LICENSE.txt` in the `assets/font` directory for details.

There is no requirements.txt because there are only four dependencies.

## Setup

From the root directory, run:

```
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install pygame-ce pyinstaller mutagen requests
python3 setup.py
python3 main.py --dev
```
NOTE: Passing the --dev flag enables developer mode on startup.
NOTE: setup.py is absolutely essential to run the program.

Feature Additions

Before adding new features, check the requested_additions file in the root directory. Try implementing one of those ideas first, then submit a pull request.

Credits

Logo designed by Reina Meza
Instagram: https://www.instagram.com/reinamariemeza/?hl=en

Soundtrack
Winter Waves — JumpyJuggernaut
Isle of Atmospheres — JumpyJuggernaut
Wobble Doom — JumpyJuggernaut
Millenia — JumpyJuggernaut
Into The Dark Void — JumpyJuggernaut
Dances With Synths — JumpyJuggernaut
Minty Awakening — JumpyJuggernaut
Lo-Fi-Si — JumpyJuggernaut
Sound Effects
Button Hover — RugerClaus
Button Click — RugerClaus
Developer Mode
Debug Overlay

When the debug overlay is active:

F8 + 1: Show all global active SYSTEM states
F8 + 2: Show all global active APPLICATION states
F8 + 3: Show all global active GAME states
F8 + 4: Show all global active states

Press F9 to display the debug overlay. This shows the current track, framerate, and the state tree for all active states, including APPSTATE and GAMESTATE.

Press F2 to enter developer mode. This will eventually allow opening a developer console and modifying game variables, including executing Python code.

Pause Menu

From the pause menu you can:

Resume the game
Restart the game
Go to the main menu
Open settings
Change sound settings and UI overlay position
Exit the program
Using the Framework

This section is a work in progress. For now, see:
https://github.com/RugerClaus/SnowBlitzProduction

Most work happens in core/game.

Start in game.py — you can structure things however you like.

State System Overview

The core runtime backbone is in core/state, based on basestatemanager.py.

You will often see patterns like:

self.system.app_state.set_state(APPSTATE.MAIN_MENU)

States are defined as enums. Each statemanager.py defines allowed transitions via a dictionary.

State Manager Concepts

Each state manager inherits from BaseStateManager and requires:

initial_state: starting state (e.g., APPSTATE.LOADING)
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

class APPSTATE(Enum):
    LOADING = auto()
    MAIN_MENU = auto()
    GAME = auto()
    QUIT = auto()
```
Example State Manager
```
from core.state.ApplicationLayer.state import APPSTATE
from core.state.basestatemanager import BaseStateManager
from helper import log_state_transition

class StateManager(BaseStateManager):
    def __init__(self):
        allowed_transitions = {
            APPSTATE.LOADING: [APPSTATE.MAIN_MENU, APPSTATE.QUIT],
            APPSTATE.MAIN_MENU: [APPSTATE.GAME, APPSTATE.QUIT],
            APPSTATE.GAME: [APPSTATE.MAIN_MENU, APPSTATE.QUIT]
        }

        super().__init__(
            initial_state=APPSTATE.LOADING,
            allowed_transitions=allowed_transitions,
            log_fn=lambda old, new, state_type: log_state_transition(old, new, state_type),
            state_name="APPSTATE",
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