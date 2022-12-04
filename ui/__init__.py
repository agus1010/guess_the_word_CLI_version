from . import *
from .cli import cli
from lowlevel import SpecialModule, import_names


class UISpecialModule(SpecialModule):
    special = {
        "cli": ".cli.cli",
    }

import_names(UISpecialModule)