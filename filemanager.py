import json
from command import Command


def read_to_list(file):
    with open(file) as f:
        commands = json.load(f)
        print(commands)
    return [Command(command["name"], command["parameters"], command["response"]) for command in commands["commands"]]


def write(file, commands):
    commands_dict = {"commands": [command.__dict__ for command in commands]}
    print(commands_dict)
    with open(file, "w") as f:
        json.dump(commands_dict, f)