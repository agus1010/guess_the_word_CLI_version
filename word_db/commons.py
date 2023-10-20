from dataclasses import dataclass
from string import ascii_lowercase

import json

from .paths import WORD_DB_STATS_PATH


ACCENTED_VOWELS = "áéíóú"

ACCENTS_REPLACE = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u"}

ACCENTLESS_GAME_CHARS = ascii_lowercase + "ñ"

ACCENTED_GAME_CHARS = ACCENTLESS_GAME_CHARS + ACCENTED_VOWELS

with open(WORD_DB_STATS_PATH, "r", encoding="utf-8") as db_stats:
    WORD_DB_STATS_RAW:dict[str:any] = json.load(db_stats)
    _word_lenghts = WORD_DB_STATS_RAW["word_lengths"]
    MIN_WORD_LENGTH = _word_lenghts["min"]
    MAX_WORD_LENGTH = _word_lenghts["max"]
