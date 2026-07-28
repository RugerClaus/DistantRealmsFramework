import pygame
import random
import os
from mutagen import File
from helper import audio_path
from systemlogging import log_error, log_event

from core.state.RuntimeLayer.state import RUNTIME_STATE
from core.state.RuntimeLayer.Audio.Interface.state import INTERFACE_SFX_STATE
from core.state.RuntimeLayer.Audio.Interface.statemanager import InterfaceSFXStateManager
from core.state.RuntimeLayer.Audio.Music.state import MUSIC_STATE
from core.state.RuntimeLayer.Audio.Music.statemanager import MusicStateManager
from core.state.RuntimeLayer.Audio.Application.state import APP_SFX_STATE
from core.state.RuntimeLayer.Audio.Application.statemanager import AppSFXStateManager
from core.state.RuntimeLayer.Audio.SFX.state import SYSTEM_SFX_STATE
from core.state.RuntimeLayer.Audio.SFX.statemanager import SystemSFXStateManager

class AudioEngine:
    def __init__(self, system):
        self.system = system
        self.runtime_state = system.runtime_state
        default_volume = 0.3
        self.create_volume_files(str(default_volume))

        self.interface_sfx_state = InterfaceSFXStateManager()
        self.music_state = MusicStateManager()
        self.game_sfx_state = AppSFXStateManager()
        self.system_sfx_state = SystemSFXStateManager()

        self.audio_available = self.initialize_audio()

        if self.audio_available:
            self.interface_sfx_state.set_state(INTERFACE_SFX_STATE.ON)
            self.music_state.set_state(MUSIC_STATE.ON)
            self.game_sfx_state.set_state(APP_SFX_STATE.ON)
            self.system_sfx_state.set_state(SYSTEM_SFX_STATE.ON)
            self.system.system_monitor["Audio"] = "Active"
        else:
            self.interface_sfx_state.set_state(INTERFACE_SFX_STATE.OFF)
            self.music_state.set_state(MUSIC_STATE.OFF)
            self.game_sfx_state.set_state(APP_SFX_STATE.OFF)
            self.system_sfx_state.set_state(SYSTEM_SFX_STATE.OFF)
            self.system.system_monitor["Audio"] = "Unavailable: No Device"

        self.music_tracks = {}
        self.sound_effects = {}
        self.active_sfx = {}
        self.volume = float(self.system.load.read_constant('music_volume'))
        self.sfx_volume = float(self.system.load.read_constant('sfx_volume'))
        self.music_queue = []
        self.current_track = None

        self.load_audio_files()

    def create_volume_files(self,default_volume):
            file_path = 'saves/constants'
            if not os.path.exists(f'{file_path}'):
                os.makedirs(f'{file_path}')
            
            if not os.path.exists(f"{file_path}/music_volume"):
                self.system.save.write_constant('music_volume',f'{default_volume}')
                log_event('Music volume file creation: music_volume file created')
            else:
                log_event('Music volume file creation: music_volume file exists')
            
            if not os.path.exists(f"{file_path}/sfx_volume"):
                self.system.save.write_constant('sfx_volume',f'{default_volume}')
                log_event('SFX volume file creation: sfx_volume file created')
            else:
                log_event('SFX volume file creation: sfx_volume file exists')

    def initialize_audio(self):
        try:
            pygame.mixer.init()
            self.MUSIC_END_EVENT = pygame.USEREVENT + 1
            pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)
            log_event("Audio device initialized successfully.")
            return True

        except pygame.error as e:
            log_error(f"No available audio device. PyGame: {e}")
            return False

    def load_audio_files(self):
        self.load_music_tracks()
        self.load_sound_effects()

    def load_music_tracks(self):
        music_dir = audio_path("music")

        for filename in os.listdir(music_dir):
            if filename.endswith(('.mp3', '.ogg', '.wav')):
                track_path = os.path.join(music_dir, filename)
                audio_file = File(track_path)
                title = audio_file.get('title', [filename])[0]
                self.music_tracks[title] = track_path

        self.music_queue = list(self.music_tracks.keys())
        random.shuffle(self.music_queue)

    def load_sound_effects(self):
        if not self.audio_available:
            log_event("Skipping sound effect loading. Audio device unavailable.")
            return

        sfx_dir = audio_path("sfx")

        for filename in os.listdir(sfx_dir):
            if filename.endswith(('.mp3', '.ogg', '.wav')):
                sfx_path = os.path.join(sfx_dir, filename)
                sound_file = File(sfx_path)
                effect_name = sound_file.get('title', [filename])[0]
                effect_name = os.path.splitext(effect_name)[0]
                self.sound_effects[effect_name] = pygame.mixer.Sound(sfx_path)

    def play_sfx(self, effect_name):
        if not self.audio_available:
            return "off"

        if self.game_sfx_state.is_state(APP_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sound_effect = self.sound_effects[effect_name]
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.game_sfx_state.is_state(APP_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
        else:
            return "off"

    def play_ui_sfx(self, effect_name):
        if not self.audio_available:
            return "off"

        if self.interface_sfx_state.is_state(INTERFACE_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sound_effect = self.sound_effects[effect_name]
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.interface_sfx_state.is_state(INTERFACE_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
        else:
            return "off"

    def play_system_sfx(self, effect_name):
        if not self.audio_available:
            return "off"

        if self.system_sfx_state.is_state(SYSTEM_SFX_STATE.ON):
            if effect_name in self.sound_effects:
                sound_effect = self.sound_effects[effect_name]
                sound_effect.set_volume(self.sfx_volume)
                sound_effect.play()
                self.active_sfx[effect_name] = sound_effect
            else:
                log_error(f"Sound effect '{effect_name}' not found.")
        elif self.system_sfx_state.is_state(SYSTEM_SFX_STATE.NONE):
            log_error("Missing sound device", "AudioEngine: cannot set sound device")
        else:
            return "off"
        
    def fade_out_music(self, duration):
        if not self.audio_available:
            return "off"

        steps = max(1, duration // 50)
        step_volume = self.volume / steps

        for i in range(steps):
            pygame.time.delay(50)
            self.volume = max(0, self.volume - step_volume)
            pygame.mixer.music.set_volume(self.volume)

        pygame.mixer.music.stop()
        self.current_track = None

    def stop_sfx(self, effect_name):
        if not self.audio_available:
            return "off"

        if effect_name in self.active_sfx:
            self.active_sfx[effect_name].stop()
            del self.active_sfx[effect_name]

    def stop_all_sfx(self):
        if not self.audio_available:
            return "off"

        log_event('Stopping all SFX')

        for sfx in self.active_sfx.values():
            sfx.stop()

        self.active_sfx.clear()

    def play_music(self, track=None):
        if not self.audio_available:
            return "off"

        if track is None:
            if not self.music_queue:
                self.music_queue = list(self.music_tracks.keys())
                random.shuffle(self.music_queue)

            track = self.music_queue.pop()

            self.current_track = track
            pygame.mixer.music.load(self.music_tracks[track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()

        elif track == "stop":
            self.music_state.set_state(MUSIC_STATE.OFF)
            self.current_track = None
            pygame.mixer.music.stop()

        else:
            matching_track = next(
                (
                    title for title in self.music_tracks
                    if title.split(" - ", 1)[0].lower() == track.lower()
                ),
                None
            )

            if matching_track is None:
                log_error(f"Music track '{track}' not found.")
                return

            self.current_track = matching_track
            pygame.mixer.music.load(self.music_tracks[matching_track])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

    def handle_music_event(self, event):
        if not self.audio_available:
            return

        if event.type == self.MUSIC_END_EVENT:
            if self.music_state.is_state(MUSIC_STATE.ON) and self.music_queue:
                self.play_music()

    def toggle_music(self):
        if not self.audio_available:
            return "off"

        if self.music_state.is_state(MUSIC_STATE.ON):
            self.play_music("stop")
            self.music_state.set_state(MUSIC_STATE.OFF)
        else:
            self.play_music()
            self.music_state.set_state(MUSIC_STATE.ON)

    def volume_up(self):
        if self.volume < 0.5:
            self.volume += 0.1
            self.volume = round(self.volume, 1)
            self.system.save.write_constant('music_volume', str(self.volume))

            if self.audio_available:
                pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        if self.volume > 0:
            self.volume -= 0.1
            self.volume = round(self.volume, 1)
            self.system.save.write_constant('music_volume', str(self.volume))

            if self.audio_available:
                pygame.mixer.music.set_volume(self.volume)

    def sfx_volume_up(self):
        if self.sfx_volume < 0.5:
            self.sfx_volume += 0.1
            self.sfx_volume = round(self.sfx_volume, 1)
            self.system.save.write_constant('sfx_volume', str(self.sfx_volume))

    def sfx_volume_down(self):
        if self.sfx_volume > 0:
            self.sfx_volume -= 0.1
            self.sfx_volume = round(self.sfx_volume, 1)
            self.system.save.write_constant('sfx_volume', str(self.sfx_volume))