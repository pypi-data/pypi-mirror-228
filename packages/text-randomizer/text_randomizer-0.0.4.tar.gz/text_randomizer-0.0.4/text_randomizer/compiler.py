import random


class Compiler:
    def __init__(self, ast: dict) -> None:
        self.__ast = ast
        self.__ast_count = 0

    def render_random_mixing_node(self, node: dict) -> str:
        random.shuffle(node['nodes'])
        render_result = ''

        for value in node['nodes']:
            if isinstance(value, str):
                render_result += value
                continue
            if value.get('type') == 'random_choice':
                render_result += self.render_random_choice_node(value)
                continue
            if value.get('type') == 'random_mixing_with_delimiter':
                render_result += self.render_random_mixing_with_delimiter_node(
                    value
                )
                continue
        return render_result

    def render_random_mixing_with_delimiter_node(self, node: dict) -> str:
        values = []

        for value in node['nodes']:
            if isinstance(value, str):
                values.append(value)
                continue
            if value.get('type') == 'random_choice':
                values.append(random.choice(value['nodes']))
        random.shuffle(values)
        render_result = node['delimiter'].join(values)
        return render_result

    def render_random_choice_node(self, node: dict) -> str:
        values = []

        for value in node['nodes']:
            if isinstance(value, str):
                values.append(value)
                continue
            if value.get('type') == 'random_choice':
                if len(values):
                    values.append(
                        values.pop() + self.render_random_choice_node(value)
                    )
                else:
                    values.append(self.render_random_choice_node(value))
                continue
            if value.get('type') == 'random_mixing':
                if len(values):
                    values.append(
                        values.pop() + self.render_random_mixing_node(value)
                    )
                else:
                    values.append(self.render_random_mixing_node(value))
                continue
            if value.get('type') == 'random_mixing_with_delimiter':
                if len(values):
                    values.append(
                        values.pop() + self.render_random_mixing_with_delimiter_node(value)
                    )
                else:
                    values.append(
                        self.render_random_mixing_with_delimiter_node(value))
                continue

        return random.choice(values)

    def render_ast(self) -> str:
        render_result = ''

        while self.__ast_count < len(self.__ast['nodes']):
            node = self.__ast['nodes'][self.__ast_count]

            if node['type'] == 'text':
                render_result += node['value']
            if node['type'] == 'random_choice':
                render_result += self.render_random_choice_node(node)
            if node['type'] == 'random_mixing':
                render_result += self.render_random_mixing_node(node)
            if node['type'] == 'random_mixing_with_delimiter':
                render_result += self.render_random_mixing_with_delimiter_node(
                    node
                )
            self.__ast_count += 1
        return render_result
