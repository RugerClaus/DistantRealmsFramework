import argparse
from core.engine.runtime import Runtime
from core.engine.system import System
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
