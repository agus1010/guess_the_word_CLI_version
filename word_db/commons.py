from string import ascii_lowercase

import json

from .paths import WORD_DB_STATS_PATH


ACCENTED_VOWELS = "áéíóú"

ACCENTS_REPLACE = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u"}

ACCENTLESS_GAME_CHARS = ascii_lowercase + "ñ"

ACCENTED_GAME_CHARS = ACCENTLESS_GAME_CHARS + ACCENTED_VOWELS


with open(WORD_DB_STATS_PATH, "r", encoding="utf-8") as db_stats:
    WORD_DB_STATS = json.load(db_stats)