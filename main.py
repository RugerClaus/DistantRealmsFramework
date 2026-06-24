import argparse
from core.guts.app import App
from core.guts.system import System
from core.state.ApplicationLayer.dev import DEVELOPER_MODE
from core.state.ApplicationLayer.state import APPSTATE

def main():
    parser = argparse.ArgumentParser(description="Game Startup")
    
    parser.add_argument('--dev', action='store_true', help="Enable developer mode. Skips the main menu and goes straight to the program.")

    args = parser.parse_args()

    system = System()
    app = App(system)

    if args.dev:
        system.control_state.set_state(DEVELOPER_MODE.ON)
        app.game.init()
    app.run()

if __name__ == "__main__":
    main()
