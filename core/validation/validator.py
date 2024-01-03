from .commons import WordValidation, WORD_VALIDATION_STATUS
from .wordfuncs import generate_checksum
from ..protocols.protocols import PGameConfig, PWordSet


class WordValidator:

    def __init__(self, game_word:str, game_config:PGameConfig, word_set:PWordSet) -> None:
        self._word = game_word
        self._config = game_config
        self._word_set = word_set
    
    def validate(self, input_word:str) -> WordValidation:
        status = WORD_VALIDATION_STATUS.CORRECT
        config = self._config

        if (input_len := len(input_word)) != config.word_length:
            if input_len < config.word_length:
                status = WORD_VALIDATION_STATUS.NOT_ENOUGH_CHARS
            else:
                status = WORD_VALIDATION_STATUS.TOO_MANY_CHARS
        elif not self._word_set.contains(input_word.strip()):
            status = WORD_VALIDATION_STATUS.WORD_NOT_IN_DICTIONARY
        
        detail = None
        if status < 10:
            detail = generate_checksum(self._word, input_word)
            status = WORD_VALIDATION_STATUS.CORRECT if sum(detail) == 0 else WORD_VALIDATION_STATUS.WRONG

        return WordValidation(input_word, detail, status)