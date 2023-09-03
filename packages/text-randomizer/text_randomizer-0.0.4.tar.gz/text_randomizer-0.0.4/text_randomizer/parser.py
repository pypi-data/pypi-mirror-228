from .lexer import Lexeme, LexemeCodes


class Parser:
    def __init__(self, lexemes: list[Lexeme]) -> None:
        self.__lexemes = lexemes
        self.__lexeme_count = 0

    def _get_current_lexeme(self) -> Lexeme:
        return self.__lexemes[self.__lexeme_count]

    def get_random_choice_ast(self) -> dict:
        random_choice_ast = {
            'type': 'random_choice'
        }

        while self.__lexeme_count < len(self.__lexemes):
            lexeme = self._get_current_lexeme()

            if lexeme.code == LexemeCodes.random_mixing_start:
                self.__lexeme_count += 1
                if random_choice_ast.get('nodes') is None:
                    random_choice_ast['nodes'] = []
                if self._get_current_lexeme().code != LexemeCodes.random_mixing_delimiter:
                    random_choice_ast['nodes'].append(
                        self.get_random_mixing_ast()
                    )
                else:
                    self.__lexeme_count += 1
                    random_choice_ast['nodes'].append(
                        self.get_random_mixing_with_delimiter_ast()
                    )
            if lexeme.code == LexemeCodes.random_choice_start:
                self.__lexeme_count += 1
                if random_choice_ast.get('nodes') is None:
                    random_choice_ast['nodes'] = []
                random_choice_ast['nodes'].append(
                    self.get_random_choice_ast()
                )
            if lexeme.code == LexemeCodes.text:
                if random_choice_ast.get('nodes') is None:
                    random_choice_ast['nodes'] = []
                random_choice_ast['nodes'].append(lexeme.value)
            if lexeme.code == LexemeCodes.random_choice_end:
                break
            self.__lexeme_count += 1
        return random_choice_ast

    def get_random_mixing_ast(self) -> dict:
        random_mixing_ast = {
            'type': 'random_mixing'
        }

        while self.__lexeme_count < len(self.__lexemes):
            lexeme = self._get_current_lexeme()

            if lexeme.code == LexemeCodes.random_choice_start:
                self.__lexeme_count += 1
                if random_mixing_ast.get('nodes') is None:
                    random_mixing_ast['nodes'] = []
                random_mixing_ast['nodes'].append(
                    self.get_random_choice_ast()
                )
            if lexeme.code == LexemeCodes.text:
                if random_mixing_ast.get('nodes') is None:
                    random_mixing_ast['nodes'] = []
                random_mixing_ast['nodes'].append(lexeme.value)
            if lexeme.code == LexemeCodes.random_mixing_end:
                break
            self.__lexeme_count += 1
        return random_mixing_ast

    def get_random_mixing_with_delimiter_ast(self) -> dict:
        random_mixing_with_delimiter_ast = {
            'type': 'random_mixing_with_delimiter'
        }

        if self._get_current_lexeme().code == LexemeCodes.random_mixing_delimiter:
            random_mixing_with_delimiter_ast['delimiter'] = ''
            self.__lexeme_count += 1
        else:
            random_mixing_with_delimiter_ast['delimiter'] = self._get_current_lexeme(
            ).value
            self.__lexeme_count += 2

        while self.__lexeme_count < len(self.__lexemes):
            lexeme = self._get_current_lexeme()

            if lexeme.code == LexemeCodes.random_choice_start:
                self.__lexeme_count += 1
                if random_mixing_with_delimiter_ast.get('nodes') is None:
                    random_mixing_with_delimiter_ast['nodes'] = []
                random_mixing_with_delimiter_ast['nodes'].append(
                    self.get_random_choice_ast()
                )
            if lexeme.code == LexemeCodes.text:
                if random_mixing_with_delimiter_ast.get('nodes') is None:
                    random_mixing_with_delimiter_ast['nodes'] = []
                random_mixing_with_delimiter_ast['nodes'].append(lexeme.value)
            if lexeme.code == LexemeCodes.random_mixing_end:
                break
            self.__lexeme_count += 1
        return random_mixing_with_delimiter_ast

    def get_ast(self) -> dict:
        ast = {
            'type': 'root',
            'nodes': []
        }

        self.__lexeme_count = 0
        while self.__lexeme_count < len(self.__lexemes):
            lexeme = self._get_current_lexeme()

            if lexeme.code == LexemeCodes.text:
                ast['nodes'].append({
                    'type': 'text',
                    'value': lexeme.value
                })
            if lexeme.code == LexemeCodes.random_choice_start:
                self.__lexeme_count += 1
                ast['nodes'].append(self.get_random_choice_ast())
            if lexeme.code == LexemeCodes.random_mixing_start:
                self.__lexeme_count += 1
                if self._get_current_lexeme().code != LexemeCodes.random_mixing_delimiter:
                    ast['nodes'].append(self.get_random_mixing_ast())
                else:
                    self.__lexeme_count += 1
                    ast['nodes'].append(
                        self.get_random_mixing_with_delimiter_ast()
                    )

            self.__lexeme_count += 1
        return ast
