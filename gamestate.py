from typing import Callable

import wordpicks
import wordutils


class GameStartConfig:
    def __init__(
            self,
            accents:bool = False,
            word_length:int = 5,
            word_picker:Callable[[bool, int],str] = wordpicks.pick_fixed_length_random_word,
            max_rounds:int = 6
        ) -> None:
        self.accents = accents
        self.word_length = word_length
        self.word_picker = word_picker
        self.max_rounds = max_rounds

    def set_dev_mode(self, debug_word:str = None):
        if debug_word != None:
            self.word_length = len(debug_word)
            self.accents = wordutils.has_accent(debug_word)
            self.word_picker = (lambda x, y: debug_word)
        


class GameState:
    def __init__(self, accents:bool, game_word:str, max_rounds:int) -> None:
        self.accents = accents
        self.word = game_word
        self.word_length = len(game_word)
        self.max_rounds = max_rounds
        self.current_round = 1