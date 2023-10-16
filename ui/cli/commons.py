from sys import stdout

from word_db.commons import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS



def print(msg:str) -> None:
    stdout.write(msg)
    stdout.flush()

def back_word(msg:str) -> str:
    return "\b" * len(msg)

def clamp_word_length(word:str, max_word_length:int, fill_with:str=" ") -> str:
    word_len = len(word)
    if word_len > max_word_length:
        return word[max_word_length:]
    elif word_len < max_word_length:
        return word + fill_with*(max_word_length - word_len)
    return word






class CLIOutputMsg:
    
    def __init__(self, line:str, new_line:bool = True, print_now:bool = False) -> None:
        self.line = line
        self._cleared = False
        self.force_new_line = new_line
        if print_now:
            self.print()

    def clear(self) -> None:
        full_back = back_word(self.line)
        full_clear = " "*len(self.line)
        print(full_back)
        print(full_clear)
        print(full_back)
        self._cleared = True

    @property
    def cleared(self) -> bool:
        return self._cleared
    
    def print(self) -> None:
        self._cleared = False
        final_msg = self.line
        if self.force_new_line:
            final_msg += "\n"
        print(final_msg)
        with open("log.log", "a", encoding="utf8") as log:
            log.writelines(final_msg)



class KeyboardManager:

    def __init__(self, max_length:int, allow_accents:bool, prev_loaded_word:str="") -> None:
        self.buffer = prev_loaded_word
        self._max_length = max_length
        self._allow_accents = allow_accents
        self._specials_lookup = {
            "enter": "\n",
            "backspace": "\b"
        }

    def on_press(self, key:str):
        alphabet = ACCENTED_GAME_CHARS if self._allow_accents else ACCENTLESS_GAME_CHARS
        if (len(self.buffer) < self._max_length) and (key in alphabet):
            self.buffer += str(key)
            print(str(key))
        if key in self._specials_lookup.keys():
            if key == "backspace":
                if len(self.buffer) > 0:
                    self.buffer = self.buffer[:-1]
                    print("\b_\b")