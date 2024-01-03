from core import PWordSet
import word_db.funcs as WordDB


class BasicWordDBSet(PWordSet):

    def __init__(self, accents:bool) -> None:
        self.accents = accents

    def contains(self, word: str) -> bool:
        return WordDB.word_is_in_dictionary(word, self.accents)



class DebugWordDBSet(BasicWordDBSet):
    def contains(self, word: str) -> bool:
        cmp = "avión" if self.accents else "avion"
        return word == cmp