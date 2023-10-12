from dataclasses import dataclass
from enum import IntEnum


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