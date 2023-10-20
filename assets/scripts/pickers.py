from random import randint

from wordle_core import PWordPicker
import wordle_core.validation.wordfuncs as WordFuncs
import word_db as WordDB



def _pick_fixed_length_random_word(accents_mode:bool, max_word_length:int) -> str:
    accents_key = "accented" if accents_mode else "accentless"
    total_word_count = WordDB.STATS["selectables"][accents_key][str(max_word_length)]
    chosen_index = randint(0, total_word_count)
    return WordDB.get_selectable_word_at_index(chosen_index, accents_mode, max_word_length)




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

    def __init__(self, word:str) -> None:
        super().__init__(accents= WordFuncs.has_accent(word), word_length= len(word))
        self.word = word

    def pick(self) -> str:
        return self.word
