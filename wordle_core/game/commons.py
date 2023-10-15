from dataclasses import dataclass
from enum import IntEnum

from ..protocols.protocols import PGameConfig


class GAME_STATUS(IntEnum):
    ON_GOING = 0
    VICTORY = 1
    DEFEAT = 2


@dataclass
class GameConfiguration(PGameConfig):
    accents: bool = False
    max_rounds:int = 6
    max_word_length:int = 5
    dev_mode:bool = False


class GameFinishedError(Exception):
    pass


class HiddenWordNotAvailable(Exception):
    pass