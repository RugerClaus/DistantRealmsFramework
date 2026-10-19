from pathlib import Path
from helper import asset
from core.util.colors import *
from systemlogging import log_warning,log_error

from core.ui.UIManager import UIManager
from core.ui.widgets.textbox import TextBox
from core.ui.widgets.scrollabletext import ScrollableText
from core.state.RuntimeLayer.DevTools.Console.state import CONSOLE_STATE


class CommandConsole:

    def __init__(self,system,position=(0.5,0.9),dimensions=(0.8,0.07),font_size=24,char_limit=256):
        self.system=system
        self.history=[]
        self.history_index=-1
        self.commands={}
        self.output_file=Path(asset("console_output"))

        self.ui_manager=UIManager(system)

        self.textbox=TextBox(
            system,
            "command_console",
            position,
            dimensions,
            font_size,
            False,
            False,
            None,
            char_limit
        )

        self.console_output=ScrollableText(
            system,
            "command_console_output",
            font_size=24,
            position=(0.48,0.75),
            width=0.8,
            height=0.2,
            source=str(self.output_file),
            vertical_align="bottom",
            direction="down"
        )

        self.ui_manager.add(self.console_output)
        self.ui_manager.add(self.textbox)

        self.textbox.set_background_color((0,0,0,180))
        self.textbox.set_text_color(white)
        self.textbox.set_border_color((0,0,0,0))
        self.textbox.set_border_width(0)

        self.create_console_log()
        self.register("help",self.help)

    def create_console_log(self):
        self.output_file.parent.mkdir(parents=True,exist_ok=True)
        self.output_file.touch(exist_ok=True)
        self.console_output.load_source(self.output_file)

    def write_output(self,text):
        with self.output_file.open("a",encoding="utf-8") as file:
            file.write(str(text)+"\n")

        self.console_output.load_source(self.output_file)

    def clear_output(self):
        self.output_file.write_text("",encoding="utf-8")
        self.console_output.load_source(self.output_file)

    def register(self,name,function):
        self.commands[name.lower()]=function

    def help(self,arguments):
        return "Commands:\n" + "\n".join(sorted(self.commands))

    def is_active(self):
        return self.system.console_state.is_state(CONSOLE_STATE.ON)

    def toggle(self):
        if self.is_active():
            self.hide()
        else:
            self.show()

    def show(self):
        self.system.console_state.set_state(CONSOLE_STATE.ON)
        self.history_index=-1
        self.textbox.set_text("")
        self.console_output.fading=False
        self.console_output.fade_start=None
        self.console_output.alpha=255
        self.ui_manager.set_active(self.textbox)

    def hide(self):
        self.system.console_state.set_state(CONSOLE_STATE.OFF)
        self.textbox.set_active(False)
        self.ui_manager.active_element=None
        self.history_index=-1
        self.console_output.fade_out(2000)

    def handle_event(self,event,command=None):
        if not self.is_active():
            return False

        if event.type==self.system.input.keydown():
            if event.key==self.system.input.keys.escape_key():
                self.textbox.set_text("")
                self.hide()
                return True

            if event.key==self.system.input.keys.enter_key():
                self.execute()
                self.hide()
                return True

            if event.key==self.system.input.keys.up_arrow_key():
                self.history_up()
                return True

            if event.key==self.system.input.keys.down_arrow_key():
                self.history_down()
                return True

        self.ui_manager.handle_event(event)

        if event.type==self.system.input.keydown():
            self.textbox.handle_event(event)

        return True

    def execute(self):
        text=self.textbox.get_return_string()

        if not text:
            return

        self.history.append(text)
        self.history_index=-1

        if text.startswith("/"):
            command=text[1:].strip()

            if not command:
                return

            self.write_output(f"> {text}")

            parts=command.split()
            name=parts[0].lower()
            arguments=parts[1:]

            function=self.commands.get(name)

            if function:
                try:
                    output=function(arguments)

                    if output is not None:
                        self.write_output(output)

                except Exception as error:
                    log_error(error)
                    self.write_output(f"Error: {error}")
            else:
                log_warning(f"Unknown command: {name}")
                self.write_output(f"Unknown command: {name}")

        else:
            self.write_output(text)

        self.textbox.set_text("")

    def history_up(self):
        if not self.history:
            return

        if self.history_index==-1:
            self.history_index=len(self.history)-1
        elif self.history_index>0:
            self.history_index-=1

        self.textbox.set_text(self.history[self.history_index])

    def history_down(self):
        if not self.history:
            return

        if self.history_index==-1:
            return

        if self.history_index<len(self.history)-1:
            self.history_index+=1
            self.textbox.set_text(self.history[self.history_index])
        else:
            self.history_index=-1
            self.textbox.set_text("")

    def update(self):
        if self.is_active():
            self.system.input.set_relative_mouse_mode(False)
            self.system.input.set_mouse_visible(True)

            self.textbox.set_active(True)
            self.textbox.update()
            self.ui_manager.update()
        else:
            self.textbox.set_active(False)
            self.console_output.update()

    def draw(self):
        self.console_output.draw()
        if self.is_active():
            self.ui_manager.draw()

    def scale(self):
        self.ui_manager.scale()