from string import ascii_lowercase

from gameglobals import ACCENTED_VOWELS


ACCENTS_REPLACE = {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u"}



def clamp_word_length(word:str, max_word_length:int) -> str:
    word_len = len(word)
    if word_len > max_word_length:
        return word[max_word_length:]
    elif word_len < max_word_length:
        return word + " "*(max_word_length - word_len)
    return word


def generate_word_ref(word:str) -> dict[str:int]:
    return { char : word.count(char) for char in word }


def has_accent(word:str) -> bool:
    for char in word:
        if char in ACCENTED_VOWELS:
            return True
    return False


def replace_accents(word:str) -> str:
    return "".join(ACCENTS_REPLACE.get(char, char) for char in word)
