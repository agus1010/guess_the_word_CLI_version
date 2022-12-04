from pathlib import Path
from sys import stdout

from colorama import init, Fore, Back, Style
from sshkeyboard import listen_keyboard

from game.errors import GameError
from game.globals import ACCENTED_GAME_CHARS, ACCENTLESS_GAME_CHARS
from game.gamestates import GameState
from ui.gui import GUI
from wordfuncs import dictionary, utils



def _print(msg:str) -> None:
    stdout.write(msg)
    stdout.flush()

# color funtions
def _cyan_f(n:str) -> str:
    return Fore.CYAN + n + Style.RESET_ALL

def _green_b(n:str) -> str:
    return Back.GREEN + n + Style.RESET_ALL

def _green_f(n:str) -> str:
    return Fore.GREEN + n + Style.RESET_ALL

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
def _back_chars(ammount:int) -> str:
    return "\b" * ammount

def _back_word(word:str) -> str:
    return _back_chars(len(word))

def _print_from_file(path:Path):
    with open(path, "r", encoding="utf-8") as src:
        for line in src.readlines():
            print(line, end="")

def _translate_type(word:str) -> str:
    return {
        "adjective": "Adjetivo",
        "adverb": "Adverbio",
        "interjection": "Interjección",
        "noun": "Sustantivo",
        "pronoun": "Pronombre",
        "verb": "Verbo"
    }.get(word, word)


init() # colorama.init()

INFO_DIR = Path("info")
USAGE = INFO_DIR / "usage.txt"
RULES = INFO_DIR / "rules.txt"
VERSION = INFO_DIR / "version"



class CLI(GUI):  #Command Line Interface

    def __init__(self) -> None:
        self._line_dirty = False
        self._prev_error_msg = ""
        self._feedback_colors = {
            0: _green_b,
            1: _yellow_b,
            2: _cli_default
        }
        self._previous_word = ""
    
    def read_player_input(self, game_state:GameState) -> str:
        self._show_current_round(game_state)
        self._show_previous_word(game_state.word)
        keyboard = KeyboardManager(game_state.word_length, game_state.accents, self._previous_word)
        self._previous_word = ""
        try:
            listen_keyboard(on_press = keyboard.on_press, until="enter", delay_other_chars=-1, delay_second_char=-1, sleep=-1, lower=True)
            self._previous_word = keyboard.buffer
            return self._previous_word.strip()
        except KeyboardInterrupt:
            self.show_end_game(game_state, player_halted=True)
            exit(1)

    def show_word_feedback(self, game_state:GameState, user_word:str, word_checksum:list[int]):
        self._previous_word = ""
        if self._line_dirty:
            self._clear_previous_error_msg()
        _print(_back_word(user_word))
        final_str = "".join(self._feedback_colors[number](char) for char, number in zip(user_word, word_checksum))
        print(final_str)
    
    def show_player_victory(self, game_state:GameState):
        print("¡Bien hecho!")
        if (original_word := self._get_original_word(game_state.word, game_state.accents)) != game_state.word:
            print(f" {_green_f(game_state.word)} ~ {_yellow_f(original_word)}")
    
    def show_player_defeat(self, game_state:GameState):
        output = "\n" + _red_f("Una lástima.. ¡Mejor suerte la próxima!")
        print(output)
        output = f"La palabra era: {_green_f(game_state.word)}"
        if (original_word := self._get_original_word(game_state.word, game_state.accents)) != game_state.word:
            output += f" ~ {_yellow_f(original_word)}"
        print(output)

    def show_start_game(self, game_state: GameState):
        print(_cyan_f("\n ¡Wordle en Casa!\n"))

    def show_end_game(self, game_state:GameState, player_halted:bool = False):
        if not player_halted:
            self.show_word_definitions(game_state)
        else:
            print(f"La palabra era: {_green_f(game_state.word)}")
        print("¡Gracias por jugar! ¡Vuelva prontos!")

    def show_game_error(self, game_state:GameState, user_word:str, error:GameError):
        if self._line_dirty:
            self._clear_previous_error_msg()
        clampped_word = utils.clamp_word_length(user_word, game_state.word_length)
        self._prev_error_msg = f" ({error.msg})" + "\r"
        error_display = _back_word(user_word) + clampped_word + self._prev_error_msg
        _print(error_display)
        self._line_dirty = True
    
    def show_word_definitions(self, game_state:GameState):
        user_input = input("¿Mostrar definiciones? (S/n): ").strip()
        if (user_input != "s" and user_input != "S"):
            return
        print("Definiciones:")
        print(_green_f(game_state.word))
        self._show_word_definitions(game_state.word)
        if not game_state.accents:
            if (original_accented := dictionary.get_original_accented_word(game_state.word)) != "":
                print("."*15)
                print(_yellow_f(original_accented))
                self._show_word_definitions(original_accented)

    @classmethod
    def show_help(cls):
        _print_from_file(USAGE)

    @classmethod
    def show_rules(cls):
        _print_from_file(RULES)
    
    @classmethod
    def show_version(cls):
        _print_from_file(VERSION)
    
    def _clear_previous_error_msg(self):
        full_clear = " "*len(self._prev_error_msg)
        full_back = _back_word(self._prev_error_msg)
        _print(full_clear)
        _print(full_back)
        self._prev_error_msg = ""
        self._line_dirty = False
    
    def _get_original_word(self, word:str, accents_mode:bool) -> str:
        if accents_mode:
            return word
        if (original_word := dictionary.get_original_accented_word(word)) != "":
            return original_word
        return word
    
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
    
    def _show_previous_word(self, game_word:str):
        if self._previous_word == "":
            round_hint = "_"*len(game_word) + _back_word(game_word)
        else:
            round_hint = utils.clamp_word_length(self._previous_word, len(game_word), fill_with="_") + _back_chars(len(game_word) - len(self._previous_word))
        _print(round_hint)
    
    def _show_word_definitions(self, word:str):
        definitions = dictionary.request_definitions(word)
        for definition in definitions:
            definition.word_types = [ _translate_type(word_type) for word_type in definition.word_types ]
            print(" • " + str(definition))



class DevCLI(CLI):
    
    def show_word_feedback(self, game_state: GameState, user_word: str, word_checksum: list[int]):
        super().show_word_feedback(game_state, user_word, word_checksum)
        print(word_checksum)

    def show_start_game(self, game_state: GameState):
        super().show_start_game(game_state)
        _print(f"Debug game: {game_state.word}\n")




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
            _print(str(key))
        if key in self._specials_lookup.keys():
            if key == "backspace":
                if len(self.buffer) > 0:
                    self.buffer = self.buffer[:-1]
                    _print("\b_\b")