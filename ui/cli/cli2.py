from sshkeyboard import listen_keyboard
from wordle_core import Wordle, WordValidation

from .commons import KeyboardManager, back_word
from .base_cli import BaseCLI

import word_db as WordDB

import ui.colourful_functions as Colors



class CLI2(BaseCLI):

    WORD_FEEDBACK_COLORS = {
        0: Colors.green_b,
        1: Colors.yellow_b,
        2: Colors.cli_default
    }


    def _show_intro(self):
        self._output(Colors.cyan_f("\n ¡Wordle!\n"))

    def _show_round_hint(self) -> None:
        current_round_msg = self._make_current_round_msg()
        round_hint = self._make_round_hint_msg()
        self.last_output.clear()
        self._output(current_round_msg + round_hint, new_line=False)

    def _show_end_game(self) -> None:
        super()._show_end_game()
        self._show_word_definitions()

    def _show_game_error(self, validation:WordValidation):
        self._clear_last_output()
        error_msg = self._last_word_read[self.game.word_length] + str(validation.status)
        self._output(error_msg)

    def _show_word_feedback(self, validation:WordValidation):
        self._clear_last_output()
        self._output("".join(CLI2.WORD_FEEDBACK_COLORS[number](char) for char, number in zip(self._last_word_read, validation.detail)))
    
    def _show_victory(self):
        self._show_end_game_msgs("¡Bien hecho!")

    def _show_defeat(self):
        self._show_end_game_msgs("\n" + Colors.red_f("Una lástima.. ¡Mejor suerte la próxima!"), f"La palabra era: {Colors.green_f(self.game.hidden_word)}")

    def _show_end_game_msgs(self, *outro_msgs):
        hidden_word = self.game.hidden_word
        original_word = self._get_original_word(hidden_word, self.accents)
        for msg in outro_msgs:
            self._output(msg)
        last_msg = f" {Colors.green_f(hidden_word)}" if original_word != hidden_word else ""
        self._output(last_msg + f" ~ {Colors.yellow_f(original_word)}")


    
    def _read_player_input(self) -> str:
        keyboard = KeyboardManager(self.game.word_length, self.accents, self._last_word_read)
        listen_keyboard(on_press = keyboard.on_press, until="enter", delay_other_chars=-1, delay_second_char=-1, sleep=-1, lower=True)
        return keyboard.buffer.strip()
    

    def _make_current_round_msg(self) -> str:
        normalized_rounds_played = self.game.rounds_played / self.game.max_rounds
        applied_color = Colors.cli_default
        if normalized_rounds_played == 1:
            applied_color = Colors.red_b
        elif normalized_rounds_played >= .81:
            applied_color = Colors.red_f
        elif normalized_rounds_played >= .51:
            applied_color = Colors.yellow_f
        return f"\r{applied_color(str(self.game.rounds_played + 1))}) "

    def _make_round_hint_msg(self) -> str:
        round_hint = self._last_word_read[self.game.word_length:]
        underscores = "_" * (self.game.word_length - len(self._last_word_read))
        round_hint += underscores
        round_hint += back_word(underscores)
        return round_hint

    def _show_word_definitions(self):
        user_input = input("¿Mostrar definiciones? (S/n): ").strip()
        if (user_input != "s" and user_input != "S"):
            return
        self._output("Definiciones:")
        hidden_word = self.game.hidden_word
        self._output(Colors.green_f(hidden_word))
        self._show_word_definitions(hidden_word)
        if not self.accents:
            if (original_accented := WordDB.get_original_accented_word(hidden_word)) != "":
                self._output("."*15)
                self._output(Colors.yellow_f(original_accented))
                self._show_word_definitions(original_accented)