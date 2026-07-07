
from datetime import datetime
import json,os

def log_error(error,object=None):
    log_file = f"logs/error.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "error": f"What happened: {error}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_event(event,object=None):
    log_file = f"logs/event.log"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "event": f"What happened: {event}"
    }
    if object is not None:
        log_data["object"] = str(object)
    with open(log_file,"a") as f:
        f.write(json.dumps(log_data) + "\n")

def log_state_transition(from_state, to_state, state_type, ticks=None, sub_dir=None, log_file=None):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": state_type,
        "ticks": ticks,
        "from": str(from_state),
        "to": str(to_state)
    }
    if sub_dir:
        log_dir = f"logs/{sub_dir}/{state_type}_Logs"
    else:
        log_dir = f"logs/{state_type}_Logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{state_type.lower()}_transitions.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data) + "\n")