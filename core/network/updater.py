# THIS FILE DOES NOTHING FOR NOW. I DON'T HAVE THE BACKEND UP FOR IT. THIS WILL COME IN A LATER UPDATE. 
# MY NEW SOLUTION IS JUST TO PATCH THE UPDATER BEFORE ANYONE ACTUALLY DOWNLOADS THE NEW VERSION FOR WINDOWS BESIDES ME
# THEN I CAN PUT THIS OFF UNTIL MACOS TIME

import os
import sys
import subprocess
import requests
import zipfile
import shutil
from helper import log_error, log_event
from config import config
from core.state.ApplicationLayer.NetworkLayer.Loading.state import FETCH_STATE
from core.state.ApplicationLayer.NetworkLayer.Loading.statemanager import FetchStateManager
from core.state.ApplicationLayer.NetworkLayer.Patch.state import PATCH_STATE
from core.state.ApplicationLayer.NetworkLayer.Patch.statemanager import PatchStateManager

TIMEOUT_SECONDS = 60

class Updater:
    def __init__(self):
        os_type = config.get("OS").lower()
        self.update_url = f"{config.get("API").get("UPDATER_FILE_URL")}/{os_type}/{config.get("UPDATER_FILE_ZIP")}"
        if not self.update_url:
            log_error("UPDATE URL url not set in config")
        self.state = PatchStateManager()
        self.fetch_state_manager = FetchStateManager()

        self.update_folder = "update"
        self.updater_zip = os.path.join(self.update_folder, "patched_updater.zip")
        self.updater_executable_name = "updater.exe"
        self.updater_executable_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), self.updater_executable_name)

        self.current_updater_version = config.get("UPDATER_VERSION")
        self.server_updater_version = None

        self.start()

    def fetch_server_updater_version(self):
        version_url = config.config.get("API").get("CURRENT_VERSION")

        try:
            response = requests.get(version_url, timeout=TIMEOUT_SECONDS)
            if response.status_code == 200:
                version_data = response.json()
                log_event(f"Fetched version data for updater. Status: {response.status_code}; Response: {version_data}")

                data = version_data.get("data", [])
                if data:
                    self.server_updater_version = data[0].get("version_number")
                else:
                    self.server_updater_version = None

                log_event(f"Server updater version: {self.server_updater_version}, Current updater version: {self.current_updater_version}")

            else:
                log_error(f"Failed to fetch updater version. HTTP {response.status_code}")
                self.server_updater_version = None

        except requests.exceptions.Timeout:
            log_error("Timeout occurred while fetching updater version.")
            self.server_updater_version = None
        except requests.exceptions.RequestException as e:
            log_error(f"Network error while fetching updater version: {e}")
            self.server_updater_version = None

    def download_updater(self):
        self.fetch_state_manager.set_state(FETCH_STATE.FETCHING)

        try:
            response = requests.get(self.update_url, timeout=TIMEOUT_SECONDS, stream=True)

            if response.status_code == 200:
                os.makedirs(self.update_folder, exist_ok=True)
                with open(self.updater_zip, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                log_event(f"Patched updater downloaded successfully to {self.updater_zip}")
                self.fetch_state_manager.set_state(FETCH_STATE.SUCCESS)
                return True
            else:
                log_error(f"Failed to download patched updater ZIP. HTTP {response.status_code}")
                self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
                return False

        except requests.exceptions.Timeout:
            log_error("Timeout occurred while downloading patched updater ZIP.")
            self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
            return False

        except requests.exceptions.RequestException as e:
            log_error(f"Network error while downloading patched updater ZIP: {e}")
            self.fetch_state_manager.set_state(FETCH_STATE.ERROR)
            return False

    def unpack_updater(self):
        if not os.path.exists(self.updater_zip):
            log_error(f"Patched updater zip not found at {self.updater_zip}")
            return False

        log_event(f"Unpacking patched updater from {self.updater_zip}...")

        try:
            with zipfile.ZipFile(self.updater_zip, "r") as zip_ref:
                zip_ref.extractall(self.update_folder)

            extracted_files = [name for name in os.listdir(self.update_folder) if name == self.updater_executable_name]
            if not extracted_files:
                log_error("No updater executable found in the patched updater zip.")
                return False

            new_updater_path = os.path.join(self.update_folder, extracted_files[0])
            if os.path.exists(self.updater_executable_path):
                os.remove(self.updater_executable_path)

            shutil.move(new_updater_path, self.updater_executable_path)
            log_event(f"Updater executable replaced successfully with {self.updater_executable_name}.")

            os.remove(self.updater_zip)
            log_event(f"Removed patched updater zip file: {self.updater_zip}")

        except zipfile.BadZipFile:
            log_error(f"Failed to unpack the patched updater: bad zip file {self.updater_zip}")
            return False
        except Exception as e:
            log_error(f"Failed to unpack the patched updater: {e}")
            return False

        return True

    def trigger_updater_and_exit(self):
        log_event(f"Launching updated updater: {self.updater_executable_path}")

        try:
            if sys.platform.startswith("win"):
                subprocess.Popen([self.updater_executable_path], shell=True)
            else:
                os.chmod(self.updater_executable_path, 0o755)
                subprocess.Popen([self.updater_executable_path])

        except Exception as e:
            log_error(f"Failed to launch updated updater: {e}")
            return

        sys.exit(0)

    def start(self):
        log_event("Starting the updater replacement process...")

        self.fetch_server_updater_version()

        if self.server_updater_version:
            if self.server_updater_version > self.current_updater_version:
                log_event(f"New updater version available: {self.server_updater_version}. Current version: {self.current_updater_version}.")
                self.state.set_state(PATCH_STATE.AVAILABLE)

                if self.download_updater():
                    if self.unpack_updater():
                        log_event("Updater replaced successfully!")
                        self.trigger_updater_and_exit()
                    else:
                        log_error("Failed to unpack and replace the updater executable.")
                        self.state.set_state(PATCH_STATE.CURRENT)
                else:
                    log_error("Failed to download the updated updater.")
                    self.state.set_state(PATCH_STATE.CURRENT)

            else:
                log_event("Updater is already up-to-date.")
                self.state.set_state(PATCH_STATE.CURRENT)
        else:
            log_error("Failed to fetch server updater version.")
            self.state.set_state(PATCH_STATE.CURRENT)
