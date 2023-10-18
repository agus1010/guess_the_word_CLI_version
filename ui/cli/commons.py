from dataclasses import dataclass
from sys import stdout

import sshkeyboard as Keyboard

from word_db.commons import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS



def print_msg(msg:str) -> None:
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





class TerminalLine:
    
    def __init__(self, line:str, new_line:bool = True, print_now:bool = False) -> None:
        self.line = line
        self.force_new_line = new_line
        self._cleared = False
        self._printed = False
        self._cursor_pos = 0
        if print_now:
            self.print()

    @property
    def cleared(self) -> bool:
        return self._cleared


    def clear(self) -> None:
        self.move_cursor(0)
        print_msg(" "*len(self.line))
        print_msg(back_word(self.line))
        self._cursor_pos = 0
        self._cleared = True
        self._printed = False

    def move_cursor(self, pos:int) -> None:
        line_len = len(self.line)
        target_pos = min(self._cursor_pos - pos, 0) if (pos < 0) else min(pos, max(pos, line_len))
        if self._cursor_pos == target_pos:
            return
        final_msg = self.line[target_pos:] if (target_pos > self._cursor_pos) else "\b" * (line_len - target_pos)
        print_msg(final_msg)
        self._cursor_pos = target_pos
        
    def print(self, force_print:bool = False) -> None:
        if self._printed and not force_print:
            self.clear()
        final_msg = self.line
        if self.force_new_line:
            final_msg += "\n"
        print_msg(final_msg)
        self._cursor_pos = len(final_msg)
        self._printed = True
        self._cleared = False