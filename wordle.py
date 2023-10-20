from wordle_core import Wordle, GameConfiguration

from assets.scripts.pickers import BasicWordDBPicker, DebugWordPicker
from assets.scripts.wordsets import BasicWordDBSet

from ui import CLI, BaseCLI


config = GameConfiguration(accents=False)
# picker = BasicWordDBPicker(accents=config.accents, word_length=config.word_length)
picker = DebugWordPicker("avión" if config.accents else "avion")
word_set = BasicWordDBSet(accents = config.accents)
wordle = Wordle(game_config=config, word_picker=picker, word_set=word_set)

# cli = BaseCLI(wordle=wordle, accents=config.accents)
cli = CLI(wordle=wordle, accents=config.accents)
cli.play()