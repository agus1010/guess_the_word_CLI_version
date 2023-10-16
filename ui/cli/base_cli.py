from wordle_core import Wordle, WordValidation

from .commons import CLIOutputMsg


class BaseCLI:

    def __init__(self, wordle:Wordle, accents:bool = False) -> None:
        self.game = wordle
        self.accents = accents
        self.outputs_log : [CLIOutputMsg] = []
        self._last_word_read = ""


    def play(self) -> None:
        self._show_intro()
        while not self.game.finished:
            while True:
                self._show_round_hint()
                try:
                    self._last_word_read = self._read_player_input()
                except KeyboardInterrupt:
                    break
                
                validation = self.game.guess(self._last_word_read)
                if validation.status >= 10:
                    self._show_game_error(validation)
                    continue
                else:
                    break
            self._show_word_feedback(validation)
        self._show_end_game()
        

    @property
    def last_output(self) -> CLIOutputMsg:
        return self.outputs_log[-1]
    
    def _output(self, msg:str, new_line:bool = True) -> None:
        self.outputs_log.append(CLIOutputMsg(msg, print_now = True, new_line = new_line))

    def _show_intro(self) -> None:
        self._output("Wordle!")

    def _show_round_hint(self) -> None:
        self._output(f"{self.game.rounds_played + 1}) ", new_line=False)

    def _read_player_input(self) -> str:
        return input()
    
    def _show_game_error(self, validation:WordValidation) -> None:
        self._output(f"  xxx  {validation.status}")
    
    def _show_word_feedback(self, validation:WordValidation) -> None:
        self._output(f"{validation.detail}")

    def _show_end_game(self) -> None:
        if self.game.status == 1:
            self._show_victory()
        else:
            self._show_defeat()
    
    def _show_victory(self) -> None:
        self._output("GANASTE!!")

    def _show_defeat(self) -> None:
        self._output(f"PERDISTE... la palabra era {self.game.hidden_word}")

    def _clear_last_output(self) -> None:
        if not (last_output := self.last_output).cleared:
            last_output.clear()