from wordle_core import PWordSet
from word_db.funcs import word_is_in_dictionary



class BasicWordDBSet(PWordSet):

    def __init__(self, accents:bool) -> None:
        self.accents = accents

    def contains(self, word: str) -> bool:
        return word_is_in_dictionary(word, self.accents)