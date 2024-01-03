from typing import Protocol


class PWordPicker(Protocol):
    def pick(self) -> str:
        ...


class PWordSet(Protocol):
    def contains(self, word:str) -> bool:
        ...


class PGameConfig(Protocol):
    @property
    def max_rounds(self) -> int:
        ...
    @property
    def word_length(self) -> int:
        ...