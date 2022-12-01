from gameerrors import UserWordError

import wordutils
import dictionary



def compare_words(game_word:str, user_word:str) -> list[int]:
    """
    0 = char in word and in right position
    1 = char in word but in wrong position
    2 = char not in word
    """
    game_word_ref = wordutils.generate_word_ref(game_word)
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


def word_is_valid(user_word:str, game_word_length:int, accents:bool):
    if (input_len := len(user_word)) != game_word_length:
        if input_len < game_word_length:
            raise UserWordError(msg="La palabra ingresada no tiene suficientes letras.", code=0)
        else:
            raise UserWordError(msg="La palabra ingresada tiene demasiadas letras.", code=1)
    if not dictionary.word_is_in_dictionary(user_word.strip(), accents):
        raise UserWordError(msg="La palabra ingresada no está en el diccionario.", code=2)
