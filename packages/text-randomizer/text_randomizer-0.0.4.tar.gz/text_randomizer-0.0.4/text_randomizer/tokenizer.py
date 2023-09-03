from .utils import remove_false_elements


class Tokenizer:
    def __init__(self, source: str) -> None:
        self.__source = source

    def get_tokens(self) -> list[str]:
        tokens = []
        token_start_index = 0
        token_end_index = 1

        for char in self.__source:
            if char in '{}[]+|':
                tokens.append(
                    self.__source[token_start_index:token_end_index - 1]
                )
                tokens.append(char)
                token_start_index = token_end_index

            if not set('{}[]+|') & set(self.__source[token_start_index:]):
                tokens.append(self.__source[token_start_index:])
                break

            token_end_index += 1

        tokens = remove_false_elements(tokens)
        return tokens
