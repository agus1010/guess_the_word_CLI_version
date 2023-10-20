from .commons import ACCENTED_VOWELS, ACCENTS_REPLACE



def clamp_word_length(word:str, max_word_length:int, fill_with:str=" ") -> str:
    word_len = len(word)
    if word_len > max_word_length:
        return word[max_word_length:]
    elif word_len < max_word_length:
        return word + fill_with*(max_word_length - word_len)
    return word


def generate_checksum(game_word:str, user_word:str) -> list[int]:
    """
    0 = char in word and in right position
    1 = char in word but in wrong position
    2 = char not in word
    """
    game_word_ref = generate_word_ref(game_word)
    result = []
    # detect 0s and 2s
    for game_char, user_char in zip(game_word, user_word):
        if game_word_ref.get(user_char, 0) == 0:
            result.append(2)
            continue
        if game_char == user_char:
            result.append(0)
            if (game_word_ref[user_char] - 1) >= 0:
                game_word_ref[user_char] -= 1
            continue
        result.append(-1)
    # detect 1s
    for user_char, number, i in zip(user_word, result, range(0, len(user_word))):
        if number == -1:
            if game_word_ref[user_char] > 0:
                result[i] = 1
                game_word_ref[user_char] -= 1    
            else:
                result[i] = 2
    return result


def generate_word_ref(word:str) -> dict[str:int]:
    return { char : word.count(char) for char in word }


def has_accent(word:str) -> bool:
    for char in word:
        if char in ACCENTED_VOWELS:
            return True
    return False


def replace_accents(word:str) -> str:
    return "".join(ACCENTS_REPLACE.get(char, char) for char in word)