from sys import argv

from ui import CLI, BaseCLI
from wordle_core import Wordle, GameConfiguration
from word_db import MIN_WORD_LENGTH, MAX_WORD_LENGTH

from assets.scripts.pickers import BasicWordDBPicker, DebugWordPicker
from assets.scripts.wordsets import BasicWordDBSet
import assets.scripts.info_displayer as INFO



LOWERED_ARGS = [ arg.lower() for arg in argv[1:] ]
FUNCTIONAL_ARGS = {
    "h": INFO.print_usage,
    "help": INFO.print_usage,
    "ayuda": INFO.print_usage,
    "r": INFO.print_rules,
    "reglas": INFO.print_rules,
    "rules": INFO.print_rules,
    "v": INFO.print_version,
    "version": INFO.print_version,
}


config = GameConfiguration()
dev_mode = False
debug_word = ""

for arg in LOWERED_ARGS:

    if (f := FUNCTIONAL_ARGS.get(arg, None)) != None:
        f()
        exit(1)

    if arg == "a" or arg == "acentos":
        config.accents = True
        continue

    arg_length = len(arg)
    
    if arg.startswith("l") or arg.startswith("largo"):
        if len(arg_split := arg.split("=")) > 1:
            length_arg = int(arg_split[1])
            config.word_length = min(MAX_WORD_LENGTH, max(length_arg, MIN_WORD_LENGTH))
        continue

    if arg.startswith("i") or arg.startswith("intentos"):
        if len(arg_split := arg.split("=")) > 1:
            config.max_rounds = max(1, int(arg_split[1]))
        continue

    if arg.startswith("debug"):
        dev_mode = True
        if len(arg_split := arg.split("=")) > 1:
            debug_word = arg_split[1]


if dev_mode:
    word = debug_word if debug_word != "" else ("avión" if config.accents else "avion")
    if debug_word == "":
        print(f"La palabra secreta es: {word}")
    picker = DebugWordPicker(word)
else:
    picker = BasicWordDBPicker(accents= config.accents, word_length= config.word_length)

word_set = BasicWordDBSet(accents = config.accents)
wordle = Wordle(game_config=config, word_picker=picker, word_set=word_set)

cli = CLI(wordle=wordle, accents=config.accents)
cli.play()