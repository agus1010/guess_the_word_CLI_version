from sys import argv

from cli import CLI, DevCLI
from game import Game
from gamestate import GameStartConfig

import wordpicks



def _clamp_int(number:int, min:int, max:int) -> int:
    if number < min:
        number = min
    elif number > max:
        number = max
    return number



functional_args = {
    "h": CLI.show_help,
    "help": CLI.show_help,
    "rules": CLI.show_rules,
    "v": CLI.show_version,
    "version": CLI.show_version,
}

lowered_args = [ arg.lower() for arg in argv[1:] ]
game_config = GameStartConfig()
dev_mode = False
debugged_word = None

for arg in lowered_args:
    if (f := functional_args.get(arg, None)) != None:
        f()
        exit(1)

    if arg == "a" or arg == "accents":
        game_config.accents = True
        continue

    arg_length = len(arg)
    
    if arg.startswith("l") or arg.startswith("length"):
        if len(arg_split := arg.split("=")) > 1:
            game_config.word_length = _clamp_int(int(arg_split[1]), 5, 10)
            game_config.word_picker = wordpicks.pick_fixed_length_random_word
        continue

    if arg.startswith("r") or arg.startswith("rounds"):
        if len(arg_split := arg.split("=")) > 1:
            game_config.max_rounds = int(arg_split[1])
        continue

    if arg.startswith("debug"):
        dev_mode = True
        if len(arg_split := arg.split("=")) > 1:
            game_config.set_dev_mode(arg_split[1])
        else:
            game_config.set_dev_mode()
        break


game = Game(
    gui = CLI() if not dev_mode else DevCLI(),
    config = game_config
)
game.play_game_loop()
