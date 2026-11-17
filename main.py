import argparse
from core.engine.runtime import Runtime
from core.engine.system import System
from core.state.SystemLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

def main():
    parser = argparse.ArgumentParser(description="Application Startup")
    
    parser.add_argument('--dev', action='store_true', help="Enable developer mode")
    parser.add_argument('--devns', action='store_true', help="Enables developer mode and skips the splash screen sequence.")

    args = parser.parse_args()

    system = System()
    runtime = Runtime(system)

    if args.dev:
        system.control_state.set_state(DEVELOPER_MODE.ON)
    elif args.devns:
        system.control_state.set_state(DEVELOPER_MODE.ON)
        system.initialize_application()
    runtime.run()

if __name__ == "__main__":
    main()
