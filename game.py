from gamestate import GameStartConfig, GameState
from gameerrors import UserWordError
from gui import GUI

import wordvalidation



class Game:
    
    def __init__(self, gui:GUI, config:GameStartConfig) -> None:
        self.game_state = GameState(
            accents = config.accents,
            game_word = config.word_picker(config.accents, config.word_length),
            max_rounds = config.max_rounds
        )
        self._gui = gui
        self.user_victory = False

    def play_round(self) -> bool:
        while True:
            user_word = self._gui.read_player_input(self.game_state)
            try:
                wordvalidation.word_is_valid(user_word, self.game_state.word_length, self.game_state.accents)
                break
            except UserWordError as uwe:
                self._gui.show_game_error(self.game_state, user_word, uwe)
        word_analysis = wordvalidation.compare_words(self.game_state.word, user_word)
        self._gui.show_word_feedback(self.game_state, user_word, word_analysis)
        return sum(word_analysis) == 0
    
    def play_game_loop(self):
        self._gui.show_start_game(self.game_state)
        while not self.user_victory and self.game_state.current_round <= self.game_state.max_rounds:
            self.user_victory = self.play_round()
            if self.user_victory:
                self._gui.show_player_victory(self.game_state)
            self.game_state.current_round += 1
        if not self.user_victory:
            self._gui.show_player_defeat(self.game_state)
        self._gui.show_end_game(self.game_state)
