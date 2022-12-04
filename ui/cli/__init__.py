from .cli import *
from lowlevel import SpecialModule, import_names


class CLISpecialModule(SpecialModule):
    special = {
        "CLI": ".CLI"
    }

import_names(CLISpecialModule)