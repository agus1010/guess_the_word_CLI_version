from dataclasses import dataclass
from sys import stdout

import sshkeyboard as Keyboard

from word_db.commons import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS



def print(msg:str) -> None:
    stdout.write(msg)
    stdout.flush()

def back_amount(amount:int) -> str:
    return "\b" * amount

def back_word(msg:str) -> str:
    return back_amount(len(msg))

def clamp_word_length(word:str, max_word_length:int, fill_with:str=" ") -> str:
    word_len = len(word)
    if word_len > max_word_length:
        return word[max_word_length:]
    elif word_len < max_word_length:
        return word + fill_with*(max_word_length - word_len)
    return word


@dataclass
class CLILine:
    rounds_played:str = ""
    word:str = ""
    error: str = ""
    cursor_pos:int = 0

    def __str__(self) -> str:
        return f"{self.rounds_played} {self.word} {self.error}"
    
    def clear(self) -> None:
        line = str(self)
        full_back = "\b" * len(line)
        full_clear = " " * len(line)
        print(full_back)
        print(full_clear)
        print(full_back)

    def move_cursor(self, pos:int) -> None:
        line = str(self)
        print("\b" * (len(line) - self.cursor_pos))

    def print(self) -> None:
        line = str(self)
        print(line)
        self.move_cursor(self.cursor_pos)
    
    def dispose(self) -> None:
        print("\n")




class TerminalLine:
    
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
    



_SPECIALS_LOOKUP = {
    "enter": "\n",
    "backspace": "\b"
}


class SingleWordInput:
    
    def __init__(self, word_length:int, accents:bool, buffer_fill:str = "_") -> None:
        self._buffer = ""
        self._max_length = word_length
        self._buffer_fill = buffer_fill
        self._alphabet = ACCENTED_GAME_CHARS if accents else ACCENTLESS_GAME_CHARS
    
    @property
    def buffer(self) -> str:
        return self._buffer
    

    @property
    def _buffer_is_full(self) -> bool:
        return len(self._buffer) >= self._max_length
    


    def input(self, preloaded_buffer_content:str = "") -> str:
        self._buffer = preloaded_buffer_content[:self._max_length]
        fill = self._buffer
        fill += self._get_buffer_fill(preloaded_buffer_content)
        fill += "\b"*self._get_buffer_fill_ammount(preloaded_buffer_content)
        print(fill)
        Keyboard.listen_keyboard(on_press = self._on_press, until="enter", delay_other_chars=-1, delay_second_char=-1, sleep=-1, lower=True)
        return self._buffer.strip()
    
    
    def _get_buffer_fill_ammount(self, buffer_content:str) -> int:
        if len(self._buffer_fill) > 0:
            return self._max_length - len(buffer_content)
        return 0
    
    def _get_buffer_fill(self, buffer_content:str) -> str:
        return self._buffer_fill * self._get_buffer_fill_ammount(buffer_content)

    def _on_press(self, input_key:str) -> None:
        if not self._buffer_is_full and (input_key in self._alphabet):
            self._buffer += str(input_key)
            print(input_key)
        if input_key == "backspace":
            if len(self._buffer) > 0:
                self._buffer = self._buffer[:-1]
                print("\b_\b")