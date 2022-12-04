from typing import Protocol

from game.gamestates import GameState
from game.errors import GameError


class GUI(Protocol):

    def read_player_input(self, gameState:GameState) -> str:
        ...

    def show_word_feedback(self, gameState:GameState, user_word:str, word_checksum:list[int]):
        ...
    
    def show_player_victory(self, gameState:GameState):
        ...
    
    def show_player_defeat(self, gameState:GameState):
        ...

    def show_start_game(self, gameState:GameState):
        ...

    def show_end_game(self, gameState:GameState):
        ...

    def show_game_error(self, gameState:GameState, user_word:str, error:GameError):
        ...
    
    @classmethod
    def show_rules(cls):
        ...