from .commons import GameConfiguration, GAME_STATUS, GameFinishedError, HiddenWordNotAvailable

from ..protocols.protocols import PWordPicker, PWordSet
from ..validation.validator import WordValidator
from ..validation.commons import WordValidation, WORD_VALIDATION_STATUS


class Wordle:
    
    def __init__(self, game_config:GameConfiguration, word_picker:PWordPicker, word_set:PWordSet) -> None:
        self._config = game_config
        self._rounds_played = 0
        self._status = GAME_STATUS.ON_GOING
        self._word = word_picker.pick()
        self._validator = WordValidator(self._word, self._config, word_set)

    @property
    def status(self) -> GAME_STATUS:
        return self._status
    
    @property
    def finished(self) -> bool:
        return self._status > 0
    
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
        return self._config.word_length
    
    @property
    def hidden_word(self) -> str:
        if not self.finished:
            raise HiddenWordNotAvailable()
        return self._word
    
    def abort(self) -> None:
        self._status = GAME_STATUS.ABORTED
    
    def guess(self, input_word:str) -> WordValidation:
        if self.finished:
            raise GameFinishedError()
        validation = self._validator.validate(input_word)
        if validation.status < 10:
            self._rounds_played += 1
            self._status = self._get_next_status(validation)
        return validation
    

    def _get_next_status(self, validation:WordValidation) -> GAME_STATUS:
        if validation.status == WORD_VALIDATION_STATUS.CORRECT:
            return GAME_STATUS.VICTORY
        if self.rounds_played == self.max_rounds:
            return GAME_STATUS.DEFEAT
        return GAME_STATUS.ON_GOING