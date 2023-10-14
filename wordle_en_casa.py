from sys import argv

from ui.cli import CLI, DevCLI

from wordle_core import Wordle
from wordle_core.game.commons import GameConfiguration
from assets.scripts.pickers import *
from assets.scripts.wordsets import *


def _clamp_int(number:int, min:int, max:int) -> int:
    if number < min:
        number = min
    elif number > max:
        number = max
    return number


functional_args = {
    "h": CLI.show_help,
    "help": CLI.show_help,
    "ayuda": CLI.show_help,
    "r": CLI.show_rules,
    "reglas": CLI.show_rules,
    "rules": CLI.show_rules,
    "v": CLI.show_version,
    "version": CLI.show_version,
}

lowered_args = [ arg.lower() for arg in argv[1:] ]
game_config = GameConfiguration()


dev_mode = False

for arg in lowered_args:
    if (f := functional_args.get(arg, None)) != None:
        f()
        exit(1)

    if arg == "a" or arg == "acentos":
        game_config.accents = True
        continue

    arg_length = len(arg)
    
    if arg.startswith("l") or arg.startswith("largo"):
        if len(arg_split := arg.split("=")) > 1:
            game_config.word_length = _clamp_int(int(arg_split[1]), 5, 10)
        continue

    if arg.startswith("i") or arg.startswith("intentos"):
        if len(arg_split := arg.split("=")) > 1:
            game_config.max_rounds = int(arg_split[1])
        continue

    if arg.startswith("debug"):
        dev_mode = True
        if len(arg_split := arg.split("=")) > 1:
            game_config.dev_mode = True
            # game_config.set_dev_mode(debug_word=arg_split[1])



word_picker = BasicWordDBPicker(accents=game_config.accents, word_length=game_config.max_rounds)
if game_config.dev_mode:
    word_picker = DebugWordPicker(accents=game_config.accents, word_length=game_config.word_length)
word_set = BasicWordDBSet(accents=game_config.accents)
game = Wordle(game_config, word_picker)