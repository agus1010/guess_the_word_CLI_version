from random import randint

from gameglobals import WORD_DB_STATS

import dictionary


def pick_fixed_length_random_word(accents_mode:bool, max_word_length:int) -> str:
    accents_key = "accented" if accents_mode else "accentless"
    chosen_index = randint(0, WORD_DB_STATS["selectables"][accents_key][str(max_word_length)])
    return dictionary.get_selectable_word_at_index(chosen_index, accents_mode, max_word_length)


def pick_random_length_random_word(accented:bool, word_length:int) -> str:
    length = randint(5, 10)
    return pick_fixed_length_random_word(max_word_length=length, accents_mode=accented)