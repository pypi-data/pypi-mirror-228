import enum


@enum.unique
class LexemeCodes(enum.Enum):
    text = 'text'
    delimiter = 'delimiter'

    random_choice_start = 'random_choice_start'
    random_choice_end = 'random_choice_end'

    random_mixing_start = 'random_mixing_start'
    random_mixing_end = 'random_mixing_end'

    random_mixing_delimiter = 'random_mixing_delimiter'


class Lexeme:
    def __init__(self, code: str, value: LexemeCodes) -> None:
        self.code = code
        self.value = value

    def __repr__(self) -> str:
        return f'<Lexeme code={self.code.name} value={self.value}>'


class Lexer:
    def __init__(self, tokens: list[str]) -> None:
        self.__tokens = tokens

    def get_lexems(self) -> list[Lexeme]:
        lexemes = []

        for token in self.__tokens:
            code = LexemeCodes.text
            if token == '|':
                code = LexemeCodes.delimiter
            if token == '{':
                code = LexemeCodes.random_choice_start
            if token == '}':
                code = LexemeCodes.random_choice_end
            if token == '[':
                code = LexemeCodes.random_mixing_start
            if token == ']':
                code = LexemeCodes.random_mixing_end
            if token == '+':
                code = LexemeCodes.random_mixing_delimiter

            lexemes.append(Lexeme(
                code=code,
                value=token
            ))
        return lexemes
