from command import Command
from pynput import keyboard
from pynput.keyboard import Controller, Key


class Keylogger:
    def __init__(self):
        self.current_command = ""
        self.commands = [Command("for", "for i in range(10):\n  "), Command("while", "while True:\n  ")]
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.controller = Controller()
        self.sending_command = False
        self.listener.start()
        self.listener.join()

    def on_key_press(self, key):
        if not self.sending_command:
            if key == keyboard.Key.space:
                self.current_command = ""
            elif key == keyboard.Key.backspace:
                self.current_command = self.current_command[:-1]
            else:
                try:
                    self.current_command += key.char
                except:
                    pass
            print(self.current_command)
            self.check_command()
        else:
            return False

    def check_command(self):
        for command in self.commands:
            if self.current_command == command.name:
                print(command.response)
                self.send_command(command)

    def send_command(self, command):
        self.listener.stop()
        for i in range(len(command.name) + 1):
            self.controller.press(Key.backspace)
            self.controller.release(Key.backspace)
        self.controller.type(command.response)
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        self.listener.join()
