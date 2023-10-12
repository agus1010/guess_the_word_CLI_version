from string import ascii_lowercase


ACCENTED_VOWELS = "áéíóú"

ACCENTS_REPLACE = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u"}

ACCENTLESS_GAME_CHARS = ascii_lowercase + "ñ"

ACCENTED_GAME_CHARS = ACCENTLESS_GAME_CHARS + ACCENTED_VOWELS