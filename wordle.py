from wordle_core import Wordle, GameConfiguration

from assets.scripts.pickers import BasicWordDBPicker
from assets.scripts.wordsets import BasicWordDBSet

from ui.cli.cli2 import CLI2


config = GameConfiguration()
picker = BasicWordDBPicker(accents=config.accents, word_length=config.word_length)
wordle = Wordle(game_config=config, word_picker=picker)

cli = CLI2(wordle=wordle, accents=config.accents)
cli.play()