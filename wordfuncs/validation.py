from . import dictionary, utils
from game.errors import UserWordError


# V2 (CORE)
from api.game.game import *
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


class WordValidator:
    def __init__(self, game_word:str, game_config:GameConfiguration) -> None:
        self._word = game_word
        self._config = game_config
    
    def validate(self, input_word:str) -> WordValidation:
        status = WORD_VALIDATION_STATUS.CORRECT
        config = self._config

        if (input_len := len(input_word)) != config.max_word_length:
            if input_len < config.max_word_length:
                status = WORD_VALIDATION_STATUS.NOT_ENOUGH_CHARS
            else:
                status = WORD_VALIDATION_STATUS.TOO_MANY_CHARS
        
        if not dictionary.word_is_in_dictionary(input_word.strip(), config.accents):
            status = WORD_VALIDATION_STATUS.WORD_NOT_IN_DICTIONARY
        
        detail = None
        if status < 10:
            detail = generate_checksum(self._word, input_word)
            status = WORD_VALIDATION_STATUS.CORRECT if sum(detail) == config.max_word_length else WORD_VALIDATION_STATUS.WRONG

        return WordValidation(detail, status)
# V2 (CORE)


def generate_checksum(game_word:str, user_word:str) -> list[int]:
    """
    0 = char in word and in right position
    1 = char in word but in wrong position
    2 = char not in word
    """
    game_word_ref = utils.generate_word_ref(game_word)
    result = []
    # detect 0s and 2s
    for game_char, user_char in zip(game_word, user_word):
        if game_word_ref.get(user_char, 0) == 0:
            result.append(2)
            continue
        if game_char == user_char:
            result.append(0)
            if (game_word_ref[user_char] - 1) >= 0:
                game_word_ref[user_char] -= 1
            continue
        result.append(-1)
    # detect 1s
    for user_char, number, i in zip(user_word, result, range(0, len(user_word))):
        if number == -1:
            if game_word_ref[user_char] > 0:
                result[i] = 1
                game_word_ref[user_char] -= 1    
            else:
                result[i] = 2
    return result


def word_is_valid(user_word:str, game_word_length:int, accents:bool):
    if (input_len := len(user_word)) != game_word_length:
        if input_len < game_word_length:
            raise UserWordError(msg="La palabra ingresada no tiene suficientes letras.", code=0)
        else:
            raise UserWordError(msg="La palabra ingresada tiene demasiadas letras.", code=1)
    if not dictionary.word_is_in_dictionary(user_word.strip(), accents):
        raise UserWordError(msg="La palabra ingresada no está en el diccionario.", code=2)
