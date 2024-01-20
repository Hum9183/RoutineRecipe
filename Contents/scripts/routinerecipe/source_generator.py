# -*- coding: utf-8 -*-
from textwrap import dedent

from .nodeeditor.connection import Connection
from .nodeeditor.node import Node
from .nodeeditor.node_state import NodeState
from .utils.routinerecipe_error import RoutineRecipeError

indent_spaces = '    '
ln = '\n'


class SourceGenerator:
    def __init__(self):
        self.__source = ''

    def generate(self, start_node: Node) -> None:
        self.__generate(start_node)
        self.__write()

    def __generate(self, start_node: Node) -> None:
        self.__source = dedent('''\
            # -*- coding: utf-8 -*-
            from maya import cmds
            ''')
        self.__add_ln()
        self.__add_ln()

        self.__source += 'def main():'

        self.__add_scripts(start_node)

    def __add_scripts(self, node: Node) -> None:
        node_state: NodeState = node.state
        connections: list[Connection] = node_state.output_connections

        if not connections:
            return

        connection: Connection = connections[0]  # とりあえず決め打ちで1つ目だけ
        input_node: Node = connection.input_node
        self.__add_ln_indent()
        self.__source += input_node.source_code()
        self.__add_ln()

        self.__add_scripts(input_node)

    def __add_ln(self) -> None:
        self.__source += ln

    def __add_ln_indent(self) -> None:
        self.__source += ln + indent_spaces

    def __write(self) -> None:
        # TODO: パスの場所をちゃんと考える
        path = r'C:\Program Files\Autodesk\ApplicationPlugins\RoutineRecipe\Contents\scripts\routinerecipe\rr_main.py'
        with open(path, mode='w') as f:
            f.write(self.__source)
