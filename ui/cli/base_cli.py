from wordle_core import Wordle, WordValidation

from .commons import CLIOutputMsg


class BaseCLI:

    def __init__(self, wordle:Wordle, accents:bool = False) -> None:
        self.game = wordle
        self.accents = accents
        self.outputs_log : list[CLIOutputMsg] = []

    @property
    def last_output(self) -> CLIOutputMsg:
        return self.outputs_log[-1]


    def play(self) -> None:
        self.show_intro()
        while not self.game.finished:
            self.show_round_hint()
            try:
                input_word = self.read_player_input()
            except KeyboardInterrupt:
                break
            validation = self.game.guess(input_word)
            self.show_input_word_feedback(validation)
        self.show_outro()
    

    def show_intro(self) -> None:
        self._output(self._get_intro_msg())

    def show_round_hint(self) -> None:
        self._output(self._get_current_round_msg(), new_line=False)
        self._output(self._get_round_hint_msg(), new_line = False)

    def read_player_input(self) -> str:
        return input()
    
    def show_input_word_feedback(self, validation:WordValidation) -> None:
        msg = validation.word
        msg += self._get_word_error_msg(validation) if validation.status >= 10 else self._get_word_feedback_msg(validation)
        self._output(msg)

    def show_outro(self) -> None:
        msg = self._get_victory_msg() if self.game.status == 1 else self._get_defeat_msg()
        self._output(msg)


    
    def _output(self, msg:str="", new_line:bool = True) -> None:
        self.outputs_log.append(CLIOutputMsg(msg, print_now = True, new_line = new_line))

    def _clear_last_output(self) -> None:
        if not (last_output := self.last_output).cleared:
            last_output.clear()
    
    
    def _get_intro_msg(self) -> str:
        return "Wordle!!"

    def _get_current_round_msg(self) -> str:
        return f"{self.game.rounds_played + 1}) "

    def _get_round_hint_msg(self) -> str:
        word_length = self.game.word_length
        return "_"*word_length + "\b"*word_length

    def _get_word_error_msg(self, validation:WordValidation) -> str:
        return f"  ERROR:  {str(validation.status)}"
    
    def _get_word_feedback_msg(self, validation:WordValidation) -> str:
        return f"  FEEDBACK:  {validation.detail}"

    def _get_victory_msg(self) -> str:
        return "GANASTE!!"
    
    def _get_defeat_msg(self) -> str:
        return f"PERDISTE... la palabra era {self.game.hidden_word}"