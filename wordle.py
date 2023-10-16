from wordle_core import Wordle, GameConfiguration

from assets.scripts.pickers import BasicWordDBPicker, DebugWordPicker
from assets.scripts.wordsets import BasicWordDBSet

from ui.cli.cli2 import CLI2
# from ui.cli.base_cli import BaseCLI


config = GameConfiguration(accents=False)
picker = DebugWordPicker(accents = config.accents, word_length=5)
word_set = BasicWordDBSet(accents = config.accents)
wordle = Wordle(game_config=config, word_picker=picker, word_set=word_set)

cli = CLI2(wordle=wordle, accents=config.accents)
cli.play()