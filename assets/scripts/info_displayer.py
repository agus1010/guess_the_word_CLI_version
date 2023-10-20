from pathlib import Path


INFO_DIR = Path("assets/info")

def _print_info(file_name:str) -> None:
    with open(INFO_DIR / file_name, "r", encoding="utf8") as info:
        for line in info.readlines():
            print(line, end="")



def print_rules() -> None:
    _print_info("rules.txt")

def print_usage() -> None:
    _print_info("usage.txt")

def print_version() -> None:
    _print_info("version")