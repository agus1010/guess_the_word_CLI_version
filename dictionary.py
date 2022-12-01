from pathlib import Path

from gameglobals import ACCENTED_LOOKUP, ACCENTLESS_LOOKUP_ORIGINALS, ACCENTLESS_LOOKUP_REPLACED, ACCENTED_SELECTABLES, ACCENTLESS_SELECTABLES

import wordutils


def get_selectable_word_at_index(index:int, accented:bool, length:int) -> str:
    target_path = (ACCENTED_SELECTABLES if accented else ACCENTLESS_SELECTABLES) / str(length)
    with open(target_path, "r", encoding="utf-8") as src:
        for i in range(0, index - 1):
            src.readline()
        return src.readline().strip()

def word_is_in_dictionary(word:str, accents_mode:bool) -> bool:
    if accents_mode:
        return _find_word_accents_mode(word)
    return _find_word_accentless_mode(word)


def _length_and_initial(word:str) -> tuple[str, str]:
    return str(len(word)), word[0]


def _word_in_file(word:str, path_to_file:Path) -> bool:
    with open(path_to_file, "r", encoding="utf-8") as src:
        while (line := src.readline().strip()) != "":
            if line == word:
                return True
    return False


def _find_word_accentless_mode(word:str) -> bool:
    word_length, first_char = _length_and_initial(word)
    path = ACCENTLESS_LOOKUP_ORIGINALS / first_char / word_length
    if _word_in_file(word, path):
        return True
    path = ACCENTLESS_LOOKUP_REPLACED / first_char / word_length
    if _word_in_file(word, path):
        return True
    return False


def _find_word_accents_mode(word:str) -> bool:
    word_length, first_char = _length_and_initial(word)
    if wordutils.has_accent(word):
        path = ACCENTED_LOOKUP / first_char / word_length
        if _word_in_file(word, path):
            return True
    else:
        path = ACCENTLESS_LOOKUP_ORIGINALS / first_char / word_length
        if _word_in_file(word, path):
            return True
    return False