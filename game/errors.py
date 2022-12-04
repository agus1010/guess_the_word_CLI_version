class GameError(Exception):
    def __init__(self, msg:str, code:int) -> None:
        self.msg = msg
        self.code = code


class UserWordError(GameError):
    pass