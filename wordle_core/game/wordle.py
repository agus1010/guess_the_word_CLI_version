from .commons import GameConfiguration, GAME_STATUS, GameFinishedError

from protocols import PWordPicker
from validation import WordValidation, WORD_VALIDATION_STATUS, WordValidator


class Wordle:
    
    def __init__(self, game_config:GameConfiguration, word_picker:PWordPicker) -> None:
        self._config = game_config
        self._rounds_played = 0
        self._status = GAME_STATUS.ON_GOING
        self._validator = WordValidator(self._word, self._config)
        self._word = word_picker.Pick()

    @property
    def status(self) -> GAME_STATUS:
        return self._status
    
    @property
    def finished(self) -> bool:
        return self.status > 0
    
    @property
    def rounds_played(self) -> int:
        return self._rounds_played

    @property
    def word_has_accents(self) -> bool:
        return self._config.accents
    
    @property
    def max_rounds(self) -> int:
        return self._config.max_rounds
    
    @property
    def word_length(self) -> int:
        return self._config.max_word_length
    
    def guess(self, input_word:str) -> WordValidation:
        if self.finished:
            raise GameFinishedError()
        validation = self._validator.validate(input_word)
        if validation.status < 10:
            self.rounds_played += 1
            self.status = self._get_next_status(validation)
        return validation
    

    def _get_next_status(self, validation:WordValidation) -> GAME_STATUS:
        if validation.status == WORD_VALIDATION_STATUS.CORRECT:
            return GAME_STATUS.VICTORY
        if self.rounds_played == self.max_rounds:
            return GAME_STATUS.DEFEAT