from pathlib import Path
from sys import stdout

from colorama import init, Fore, Back, Style
from sshkeyboard import listen_keyboard

from gameerrors import GameError
from gamestate import GameState
from gui import GUI
from gameglobals import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS

import dictionary
import wordutils



def _print(msg:str) -> None:
    stdout.write(msg)
    stdout.flush()

# color funtions
def _green_b(n:str) -> str:
    return Back.GREEN + n + Style.RESET_ALL

def _yellow_f(n:str) -> str:
    return Fore.YELLOW + n + Style.RESET_ALL 

def _yellow_b(n:str) -> str:
    return Back.YELLOW + Fore.BLACK + n + Style.RESET_ALL

def _red_f(n:str) -> str:
    return Fore.RED + n + Style.RESET_ALL

def _red_b(n:str) -> str:
    return Back.RED + Fore.BLACK + n + Style.RESET_ALL

def _cli_default(n:str) -> str:
    return n

# utils
def _back_chars(word:str) -> str:
    return "\b" * len(word)

def _print_from_file(path:Path):
    with open(path, "r", encoding="utf-8") as src:
        for line in src.readlines():
            print(line)

def _translate_type(word:str) -> str:
    return {
        "adjective": "Adj",
        "adverb": "Adv",
        "interjection": "Int",
        "noun": "Sus",
        "pronoun": "Pro",
        "verb": "Ver"
    }[word]


init() # colorama.init()

HELP_DIR = Path("help")
USAGE = HELP_DIR / "usage.txt"
RULES = HELP_DIR / "rules.txt"



class CLI(GUI):  #Command Line Interface

    def __init__(self) -> None:
        self._line_dirty = False
        self._prev_error_msg = ""
        self._feedback_colors = {
            0: _green_b,
            1: _yellow_b,
            2: _cli_default
        }
    
    def read_player_input(self, game_state:GameState) -> str:
        self._show_current_round(game_state)
        round_hint = "_"*len(game_state.word) + _back_chars(game_state.word)
        _print(round_hint)
        keyboard = KeyboardManager(game_state.word_length, game_state.accents)
        try:
            listen_keyboard(on_press = keyboard.on_press, until='enter', delay_other_chars=-1, delay_second_char=-1, sleep=-1, lower=True)
            user_word = keyboard.buffer
            return user_word.strip()
        except KeyboardInterrupt:
            self._clear_previous_error_msg()
            self.show_end_game(game_state)
            exit(-1)

    def show_word_feedback(self, game_state:GameState, user_word:str, word_analysis:list[int]):
        if self._line_dirty:
            self._clear_previous_error_msg()
        _print(_back_chars(user_word))
        final_str = "".join(self._feedback_colors[number](char) for char, number in zip(user_word, word_analysis))
        print(final_str)
    
    def show_player_victory(self, game_state:GameState):
        print("")
        print("BIEN AHIIII LA RE PEGASTE!!!")
    
    def show_player_defeat(self, game_state:GameState):
        print()
        print("mal ahí....")
        print(f"La palabra era: {game_state.word}")

    def show_start_game(self, game_state: GameState):
        pass

    def show_end_game(self, game_state:GameState):
        self.show_word_definition(game_state)
        print("\nGracias por jugar! Vuelva prontos!\n")

    def show_game_error(self, game_state:GameState, user_word:str, error:GameError):
        if self._line_dirty:
            self._clear_previous_error_msg()
        clampped_word = wordutils.clamp_word_length(user_word, game_state.word_length)
        self._prev_error_msg = f" ({error.msg})" + "\r"
        error_display = _back_chars(user_word) + clampped_word + self._prev_error_msg
        _print(error_display)
        self._line_dirty = True
    
    def show_word_definition(self, game_state:GameState):
        definitions = dictionary.request_definitions(game_state.word, game_state.accents)
        for definition in definitions:
            print(definition)
            gender = definition["category"]["abbr"]
            word_types = [ _translate_type(elem) for elem in definition["is"] if elem == True ]
            text = definition["sentence"]["text"]
            print(f"  {gender} " + ", ".join(word_types) + f": {text}")


    @classmethod
    def show_help(cls):
        _print_from_file(USAGE)

    @classmethod
    def show_rules(cls):
        _print_from_file(RULES)
    
    @classmethod
    def show_version(cls):
        _print_from_file(Path("version"))
    
    
    def _clear_previous_error_msg(self):
        full_clear = " "*len(self._prev_error_msg)
        full_back = _back_chars(self._prev_error_msg)
        _print(full_clear)
        _print(full_back)
        self._prev_error_msg = ""
        self._line_dirty = False
    
    def _show_current_round(self, game_state:GameState):
        rounds_played_percentage = game_state.current_round * 100 / game_state.max_rounds
        applied_color = None
        if game_state.max_rounds == game_state.current_round:
            applied_color = _red_b
        else:
            if rounds_played_percentage >= 81:
                applied_color = _red_f
            else:
                if rounds_played_percentage >= 51:
                    applied_color = _yellow_f
                else:
                    applied_color = _cli_default
        colored_round = f"\r{applied_color(str(game_state.current_round))}) "
        _print(colored_round)




class DevCLI(CLI):
    
    def show_word_feedback(self, game_state: GameState, user_word: str, word_analysis: list[int]):
        super().show_word_feedback(game_state, user_word, word_analysis)
        print(word_analysis)

    def show_start_game(self, game_state: GameState):
        super().show_start_game(game_state)
        _print(f"Debug game: {game_state.word}\n")




class KeyboardManager:

    def __init__(self, max_length:int, allow_accents:bool) -> None:
        self.buffer = ""
        self._max_length = max_length
        self._allow_accents = allow_accents
        self._specials_lookup = {
            "enter": "\n",
            "backspace": "\b"
        }

    def on_press(self, key_arg):
        key = str(key_arg).lower()
        alphabet = ACCENTED_GAME_CHARS if self._allow_accents else ACCENTLESS_GAME_CHARS
        if (len(self.buffer) < self._max_length) and (key in alphabet):
            self.buffer += str(key)
            _print(str(key))
        if key in self._specials_lookup.keys():
            if key == "backspace":
                if len(self.buffer) > 0:
                    self.buffer = self.buffer[:-1]
                    _print("\b_\b")