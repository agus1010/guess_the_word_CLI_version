from pathlib import Path

import json


WORD_DB_HOME = Path(".")

LOOKUP = WORD_DB_HOME / "lookup"
ACCENTED_LOOKUP = LOOKUP / "accented"
_accentless_lookup = LOOKUP / "accentless"
ACCENTLESS_LOOKUP_ORIGINALS = _accentless_lookup / "original"
ACCENTLESS_LOOKUP_REPLACED = _accentless_lookup / "accent_replaced"

SELECTABLES = WORD_DB_HOME / "selectables"
ACCENTED_SELECTABLES = SELECTABLES / "accented"
ACCENTLESS_SELECTABLES = SELECTABLES / "accentless"

WORD_DB_STATS_PATH = WORD_DB_HOME / "word_db_stats.json"

with open(WORD_DB_STATS_PATH, "r", encoding="utf-8") as db_stats:
    WORD_DB_STATS = json.load(db_stats)