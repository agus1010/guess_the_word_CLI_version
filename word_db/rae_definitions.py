from dataclasses import dataclass
from pyrae import dle
from pyrae.core import SearchResult


@dataclass
class RAEDefinition:
    word:str
    supplementary_info:list[str]
    explanations:list[str]


@dataclass
class RAEWord:
    word:str
    definitions:list[RAEDefinition]

    def pretty_str(self) -> str:
        pretty_msg = f"{self.word}\n"
        if len(self.definitions) > 0:
            for definition in self.definitions:
                sup_info = ", ".join((str(info) for info in definition.supplementary_info))
                pretty_msg += f"• {sup_info}\n"
                for explanation in definition.explanations:
                    pretty_msg += f"   {explanation}\n"
        else:
            pretty_msg += "No definitions available.\n"
        return pretty_msg



def _search_word(word:str) -> SearchResult:
    dle.set_log_level("ERROR")
    return dle.search_by_word(word)


def search_word(word:str) -> RAEWord:
    search = _search_word(word)
    definitions = []
    for article in search.articles:
        sup_info = [str(info) for info in article.supplementary_info]
        explanations = [definition.raw_text for definition in article.definitions]
        definitions.append(RAEDefinition(word= word, supplementary_info= sup_info, explanations= explanations))
    return RAEWord(word= word, definitions= definitions)




    


    


if __name__ == "__main__":
    searches = { word:_search_word(word) for word in ("avión", "agua", "enano", "cabro", "cobra")}
    articles = { word:search.to_dict() for word, search in searches.items() }

    for word, search in searches.items():
        print(f"{word}:")
        for article in search.articles:
            supplementary_info = ", ".join((str(info) for info in article.supplementary_info))
            print(f"• ({supplementary_info})")
            for definition in article.definitions:
                print(f"  {definition.raw_text}")