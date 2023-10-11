from .errors import UserWordError
from wordfuncs import validation


from dataclasses import dataclass
@dataclass
class GameConfiguration:
    accents: bool = False
    max_rounds:int = 6
    max_word_length:int = 5



class WordPicker:
    def Pick(self) -> str:
        return ""



class Game:
    
    def __init__(self, game_config:GameConfiguration) -> None:
        self.current_rounds = 0
        self.player_victory = False
        self.config = game_config
        self._word = word_picker.Pick()


    def Guess(self, word:str) -> [bool]:
        pass