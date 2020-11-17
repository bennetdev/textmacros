from command import Command
from pynput import keyboard
from pynput.keyboard import Controller, Key
import time


class Keylogger:
    def __init__(self):
        self.current_command = ""
        self.commands = [Command("for", ["d"], "for i in range($d):\n  "),
                         Command("fori", ["d"], "for i in $d:\n  "),
                         Command("class", ["d"], "class $d:\n  def __init__(self):\n    "),
                         Command("forp", ["d"], "for i in range($d):\n  print(i)"),
                         Command("get", ["d"], "def get_$d():\n   return self.$d"),
                         Command("set", ["d"], "def set_$d($d):\n   self.$d = $d"),
                         Command("while", ["d"], "while $d:\n  ")]
        self.commands.sort(key=lambda x: len(x.name), reverse=True)
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.controller = Controller()
        self.sending_command = False
        self.listener.start()
        self.listener.join()

    def on_key_press(self, key):
        if not self.sending_command:
            if key == keyboard.Key.space:
                for command in self.commands:
                    if command.matches(self.current_command):
                        print(self.current_command)
                        param = self.current_command.split(command.name)[1]
                        for i in range(len(self.current_command) + 1):
                            self.controller.tap(Key.backspace)
                        self.controller.type(command.get_response(param))
                        break
                self.current_command = ""
            elif key == keyboard.Key.backspace:
                pass
            else:
                try:
                    self.current_command += key.char
                except:
                    self.current_command = ""

    def check_command(self):
        print("check")
        for command in self.commands:
            if self.current_command == command.name:
                print(command.response)
                self.send_command(command)

    def send_command(self, command):
        self.current_command = ""
        self.sending_command = True
        self.controller.press(Key.backspace)
        self.controller.release(Key.backspace)
        self.controller.type(command.response)
        self.sending_command = False
