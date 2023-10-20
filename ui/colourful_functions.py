from colorama import init, Fore, Back, Style
from pathlib import Path



# color funtions
def cyan_f(n:str) -> str:
    return Fore.CYAN + n + Style.RESET_ALL

def green_b(n:str) -> str:
    return Back.GREEN + n + Style.RESET_ALL

def green_f(n:str) -> str:
    return Fore.GREEN + n + Style.RESET_ALL

def yellow_f(n:str) -> str:
    return Fore.YELLOW + n + Style.RESET_ALL 

def yellow_b(n:str) -> str:
    return Back.YELLOW + Fore.BLACK + n + Style.RESET_ALL

def red_f(n:str) -> str:
    return Fore.RED + n + Style.RESET_ALL

def red_b(n:str) -> str:
    return Back.RED + Fore.BLACK + n + Style.RESET_ALL

def cli_default(n:str) -> str:
    return n




# utils
def _back_chars(ammount:int) -> str:
    return "\b" * ammount

def _back_word(word:str) -> str:
    return _back_chars(len(word))

def _print_from_file(path:Path):
    with open(path, "r", encoding="utf-8") as src:
        for line in src.readlines():
            print(line, end="")