from . import *
from .game import Game
from lowlevel import SpecialModule, import_names


class GameSpecialModule(SpecialModule):
    special = {
        "Game":".game.Game"
    }

import_names(GameSpecialModule)