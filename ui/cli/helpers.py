import sshkeyboard as Keyboard
from word_db.commons import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS

from .commons import print_msg


_SPECIALS_LOOKUP = {
    "enter": "\n",
    "backspace": "\b"
}


class CLIWordInput:
    
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
        print_msg(fill)
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
            print_msg(input_key)
        if input_key == "backspace":
            if len(self._buffer) > 0:
                self._buffer = self._buffer[:-1]
                print_msg("\b_\b")