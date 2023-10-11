from dataclasses import dataclass
from enum import IntEnum
from string import ascii_lowercase


ACCENTED_VOWELS = "áéíóú"
ACCENTLESS_GAME_CHARS = ascii_lowercase + "ñ"
ACCENTED_GAME_CHARS = ACCENTLESS_GAME_CHARS + ACCENTED_VOWELS
ACCENTS_REPLACE = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u"}


class WORD_VALIDATION_STATUS(IntEnum):
    CORRECT = 0
    WRONG = 1
    WORD_NOT_IN_DICTIONARY = 11
    NOT_ENOUGH_CHARS = 20
    TOO_MANY_CHARS = 21


@dataclass
class WordValidation:
    detail:list[int]
    status:WORD_VALIDATION_STATUS