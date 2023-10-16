from sshkeyboard import listen_keyboard
from wordle_core import WordValidation, Wordle

from .commons import KeyboardManager, back_word
from .base_cli import BaseCLI

import word_db as WordDB
import ui.colourful_functions as Colors


WORD_FEEDBACK_COLORS = {
        0: Colors.green_b,
        1: Colors.yellow_b,
        2: Colors.cli_default
    }


class CLI2(BaseCLI):

    def __init__(self, wordle: Wordle, accents: bool = False) -> None:
        super().__init__(wordle, accents)
        self._last_validation = WordValidation("", [], 0)
        self.keyboard = KeyboardManager(self.game.word_length, self.accents, self._last_word_read)
        
    @property
    def _last_word_read(self) -> str:
        return self._last_validation.word


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


 
    # public overrides:

    def show_round_hint(self) -> None:
        if self._last_validation.status > 10:
            return
        super().show_round_hint()

    def read_player_input(self) -> str:
        listen_keyboard(on_press = self.keyboard.on_press, until="enter", delay_other_chars=-1, delay_second_char=-1, sleep=-1, lower=True)
        input_word = self.keyboard.buffer.strip()
        self.last_output.line = input_word
        return input_word
    
    def show_input_word_feedback(self, validation: WordValidation) -> None:
        self._last_validation = validation
        error_detected = validation.status > 10
        
        last_output = self.last_output
        if not error_detected:
            last_output.clear()
            msg = self._get_word_feedback_msg(validation)
            self._output(msg= msg, new_line= not error_detected)
        else:
            self._clear_last_output()
            last_output.line += self._get_word_error_msg(validation)
            last_output.line += back_word(last_output.line)
            last_output.print()


    def show_outro(self) -> None:
        super().show_outro()
        self._show_word_definitions()

    
    # private overrides:
    
    def _get_intro_msg(self) -> str:
        return f"\n{Colors.cyan_f('¡Wordle!')}\n"
    
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
        return f"{applied_color(displayed_number)}) "
    
    def _get_word_feedback_msg(self, validation: WordValidation) -> str:
        return "".join(WORD_FEEDBACK_COLORS[number](char) for char, number in zip(self._last_word_read, validation.detail))

    def _get_victory_msg(self) -> str:
        return "¡Bien hecho!"

    def _get_defeat_msg(self) -> str:
        intro = Colors.red_f("Una lástima.. ¡Mejor suerte la próxima!")
        outro = f"La palabra era: {Colors.green_f(self.game.hidden_word)}"
        return f"{intro}. {outro}"