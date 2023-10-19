from pyrae import dle



class RAEWordDefinition:

    def __init__(self, word:str) -> None:
        self.word_types:list[str]
        self.abbreviation: str
        self.explanation:str
        self.translate:bool = False

    def __str__(self) -> str:
        joined_types = ', '.join(translate_word_type(*self.word_types))
        return f"{joined_types} -> {self.abbr} {self.explanation}"



class WordDefinition:
    
    def __init__(self, word_types:list[str], abbr:str, explanation:str, translate:bool = False) -> None:
        self.word_types = word_types
        self.abbr = abbr
        self.translate = translate
        self.explanation = explanation
    
    def __str__(self) -> str:
        return f"{', '.join(translate_word_type(*self.word_types))} -> {self.abbr} {self.explanation}"



def request_definitions(word:str) -> list[WordDefinition]:
    dle.set_log_level("ERROR")
    resp = dle.search_by_word(word)
    resp_dict = resp.to_dict()
    result = []
    if resp_dict.get("articles", None) == None:
        return result
    for article in resp_dict["articles"]:
        definitions = _extract_definitions(article)
        for definition in definitions:
            result.append(definition)
    return result


WORD_TYPES_TRANSLATIONS = {
    "adjective": "Adjetivo",
    "adverb": "Adverbio",
    "interjection": "Interjección",
    "noun": "Sustantivo",
    "pronoun": "Pronombre",
    "verb": "Verbo"
}

def translate_word_type(word:str) -> str:
    return WORD_TYPES_TRANSLATIONS.get(word, word)


def _extract_definition_word_types(definition:dict) -> list:
    return [key for key, value in definition["is"].items() if value]


def _extract_definition_abbr(definition:dict) -> str:
    return definition["category"]["abbr"]


def _extract_definition_explanation(definition:dict) -> str:
    return definition["sentence"]["text"]


def _extract_worddefinition_obj(definition:dict) -> WordDefinition:
    return WordDefinition(
        word_types = _extract_definition_word_types(definition),
        abbr = _extract_definition_abbr(definition),
        explanation = _extract_definition_explanation(definition)
    )


def _extract_definitions(article:dict) -> list[WordDefinition]:
    return [_extract_worddefinition_obj(definition) for definition in article["definitions"]]
