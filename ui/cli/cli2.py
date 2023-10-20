from wordle_core import WordValidation, Wordle

from .base_cli import BaseCLI
from .commons import print_msg
from .helpers import CLIWordInput

import ui.colourful_functions as Colors
import word_db as WordDB
import word_db.rae_definitions as RAE


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



    def _ask_player_for_definitions(self) -> bool:
        self._output(msg= "¿Mostrar definiciones? (S/n): ", new_line= False)
        self.keyboard = CLIWordInput(word_length= 1, accents=False, buffer_fill=" ")
        user_selection = self.keyboard.input().strip().lower()
        self.last_output.line += user_selection
        self.last_output.clear()
        return user_selection == "s"

    def _output_rae_word(self, rae_word:RAE.RAEWord, word_color) -> None:
        if len(rae_word.definitions) == 0:
            return
        pretty_lines = rae_word.pretty_str().splitlines()
        pretty_lines[0] = f"{word_color(rae_word.word)}:"
        for line in pretty_lines:
            self._output(msg= line, new_line= True)


    def show_word_definitions(self, word:str):
        if not self._ask_player_for_definitions():
            return
        hidden_word = self.game.hidden_word
        original_accented = WordDB.get_original_accented_word(hidden_word)
        hidden_rae_word = RAE.search_word(hidden_word)
        original_rae_word = RAE.search_word(original_accented)
        hidden_word_defs_count = len(hidden_rae_word.definitions)
        if hidden_word_defs_count > 0:
            self._output_rae_word(hidden_rae_word, Colors.green_f)
        # accents check
        if original_accented == "" or hidden_word == original_accented:
            return
        if hidden_word_defs_count > 0:
            self._output("."*15)
        self._output_rae_word(original_rae_word, Colors.yellow_f)


    


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

    def show_outro(self) -> None:
        self._output(msg= "\n", new_line= True)
        super().show_outro()
        if self.game.status < 3:
            self.show_word_definitions(self.game.hidden_word)
        

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
        error_msg = ""
        if validation.status >= 10:
            error_formatted = self._format_error_msg(validation)
            error_msg = f"   {Colors.red_f(error_formatted)}"
        return error_msg

    def _get_word_feedback_msg(self, validation: WordValidation) -> str:
        if validation.status >= 10:
            return validation.word[:self.game.word_length] + _FILL * (self.game.word_length - len(validation.word))
        return "".join(WORD_FEEDBACK_COLORS[number](char) for char, number in zip(self._last_word_read, validation.detail))

    def _get_victory_msg(self) -> str:
        waves1 = Colors.cyan_f("°º¤ø,¸¸,ø¤º°`°º¤ø")
        waves2 = Colors.cyan_f("ø¤°º¤ø,¸¸,ø¤º°`°º")
        well_done = Colors.green_f("¡Bien hecho!")
        return f"{waves1} {well_done} {waves2}\n"

    def _get_defeat_msg(self) -> str:
        intro = Colors.red_f("Una lástima.. ¡Mejor suerte la próxima!")
        outro = f"La palabra era: {Colors.green_f(self.game.hidden_word)}"
        return f"{intro}. {outro}\n"
    
    def _format_error_msg(self, validation:WordValidation) -> str:
        msg = "La palabra "
        match validation.status:
            case 11:
                msg += "no está en el diccionario."
            case 20:
                msg += f"no tiene suficientes letras ({len(validation.word)}/{self.game.word_length})"
            case 21:
                msg += f"tiene demasiadas letras ({len(validation.word)}/{self.game.word_length})"
        return msg