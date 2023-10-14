from random import randint

from wordle_core import PWordPicker
from word_db import STATS, get_selectable_word_at_index



def _pick_fixed_length_random_word(accents_mode:bool, max_word_length:int) -> str:
    accents_key = "accented" if accents_mode else "accentless"
    chosen_index = randint(0, STATS["selectables"][accents_key][str(max_word_length)])
    return get_selectable_word_at_index(chosen_index, accents_mode, max_word_length)




class BasicWordDBPicker(PWordPicker):
    
    def __init__(self, accents:bool, word_length:int) -> None:
        self.accents = accents
        self.length = word_length

    def pick(self) -> str:
        return _pick_fixed_length_random_word(self.accents, self.length)




class RandomLengthWordPicker(BasicWordDBPicker):
    
    def __init__(self, accents: bool) -> None:
        super().__init__(accents, randint(5, 10))



class DebugWordPicker(BasicWordDBPicker):

    def pick(self) -> str:
        return "avión" if self.accents else "avion"
