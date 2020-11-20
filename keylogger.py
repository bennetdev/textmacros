from command import Command
from pynput import keyboard
from pynput.keyboard import Controller, Key
from filemanager import read_to_list, write


class Keylogger:
    def __init__(self):
        self.current_command = ""
        self.commands = read_to_list("macros.json")
        self.commands.sort(key=lambda x: len(x.name), reverse=True)
        self.categories = self.get_categories()
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.controller = Controller()
        self.sending_command = False

    def start(self, category=None):
        if category is not None:
            self.commands = self.get_commands_by_category(category)
        self.listener.start()
        self.listener.join()

    def on_key_press(self, key):
        if not self.sending_command:
            if key == keyboard.Key.space:
                print(self.current_command)
                for command in self.commands:
                    if command.matches(self.current_command):
                        print(self.current_command)
                        params = self.current_command.split(command.name)[1].split("$")
                        for i in range(len(self.current_command) + 1):
                            self.controller.tap(Key.backspace)
                        self.controller.type(command.get_response(params))
                        break
                self.current_command = ""
            elif key == keyboard.Key.backspace:
                pass
            elif key == keyboard.Key.shift:
                pass
            elif key == keyboard.Key.f8:
                exit(0)
            else:
                try:
                    self.current_command += key.char
                except:
                    self.current_command = ""

    def get_categories(self):
        return list(set([command.category for command in self.commands]))

    def check_command(self):
        print("check")
        for command in self.commands:
            if self.current_command == command.name:
                print(command.response)
                self.send_command(command)

    def get_commands_by_category(self, category):
        return [command for command in self.commands if command.category == category]

    def get_commands_except_category(self, category):
        return [command for command in self.commands if command.category != category]

    def add_macro(self, name, parameters, response):
        self.commands.append(Command(name, parameters, response))
        write("macros.json", self.commands)

    def send_command(self, command):
        self.current_command = ""
        self.sending_command = True
        self.controller.press(Key.backspace)
        self.controller.release(Key.backspace)
        self.controller.type(command.response)
        self.sending_command = False
