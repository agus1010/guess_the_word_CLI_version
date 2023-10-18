from wordle_core import WordValidation, Wordle

from .commons import print_msg
from .helpers import CLIWordInput
from .base_cli import BaseCLI

import ui.colourful_functions as Colors
import word_db as WordDB


WORD_FEEDBACK_COLORS = {
        0: Colors.green_b,
        1: Colors.yellow_b,
        2: Colors.cli_default
    }


_FILL = "_"


class CLI2(BaseCLI):

    def __init__(self, wordle: Wordle, accents: bool = False) -> None:
        super().__init__(wordle, accents)
        self.keyboard = CLIWordInput(self.game.word_length, self.accents, _FILL)
        self._current_validation = WordValidation("", [], 0)
        self._current_word_hint = ""
        self._current_error_msg = ""
        
    @property
    def _last_word_read(self) -> str:
        return self._current_validation.word


    def show_word_definitions(self, word:str):
        user_input = input("¿Mostrar definiciones? (S/n): ").strip()
        if (user_input != "s" and user_input != "S"):
            return
        self._output("Definiciones:")
        hidden_word = self.game.hidden_word
        self._output(Colors.green_f(hidden_word))

        definitions = WordDB.request_definitions(hidden_word)
        #            print(" • " + str(definition))
        
        if not self.accents:
            if (original_accented := WordDB.get_original_accented_word(hidden_word)) != "":
                self._output("."*15)
                self._output(Colors.yellow_f(original_accented))
                self.__show_word_definitions(original_accented)


    def _get_original_word(self, word:str, accents_mode:bool) -> str:
        if accents_mode:
            return word
        if (original_word := WordDB.get_original_accented_word(word)) != "":
            return original_word
        return word

    @property
    def _last_validation_has_errors(self) -> bool:
        return self._current_validation.status > 10
    

    # public overrides

    def show_round_hint(self) -> None:
        if self._current_validation.status < 10:
            self._output(msg = "", new_line= True)
            self._output(msg = self._get_current_round_msg(), new_line= False)
            self._output(msg = "", new_line= False, print_now=False)

    def read_player_input(self) -> str:
        self.last_output.move_cursor(0)
        input_msg = self._current_validation.word if self._current_validation.status >= 10 else ""
        input_word = self.keyboard.input(input_msg)
        print_msg("\b"*len(input_word))
        return input_word
    
    def validate_word(self, word: str) -> WordValidation:
        self._current_validation = super().validate_word(word)
        return self._current_validation
    
    def show_input_word_feedback(self, validation: WordValidation) -> None:
        self._current_word_hint = self._get_word_feedback_msg(validation)
        self._current_error_msg = self._get_word_error_msg(validation)
        self.last_output.clear()
        final_msg = f"{self._current_word_hint} {self._current_error_msg}"
        self._output(final_msg, new_line= False)


    # private overrides:
    
    def _get_intro_msg(self) -> str:
        return f"\n{Colors.cyan_f('¡Wordle!')}"
    
    def _get_current_round_msg(self) -> str:
        normalized_rounds_played = self.game.rounds_played / self.game.max_rounds
        applied_color = Colors.cli_default
        if normalized_rounds_played == 1:
            applied_color = Colors.red_b
        elif normalized_rounds_played >= .81:
            applied_color = Colors.red_f
        elif normalized_rounds_played >= .51:
            applied_color = Colors.yellow_f
        displayed_number = self.game.rounds_played + 1
        return f"{applied_color(str(displayed_number))}) "

    def _get_word_error_msg(self, validation: WordValidation) -> str:
        return super()._get_word_error_msg(validation) if validation.status >= 10 else ""

    def _get_word_feedback_msg(self, validation: WordValidation) -> str:
        if validation.status >= 10:
            return validation.word[:self.game.word_length] + _FILL * (self.game.word_length - len(validation.word))
        return "".join(WORD_FEEDBACK_COLORS[number](char) for char, number in zip(self._last_word_read, validation.detail))

    def _get_victory_msg(self) -> str:
        return "¡Bien hecho!"

    def _get_defeat_msg(self) -> str:
        intro = Colors.red_f("Una lástima.. ¡Mejor suerte la próxima!")
        outro = f"La palabra era: {Colors.green_f(self.game.hidden_word)}"
        return f"{intro}. {outro}"