# -*- coding: utf-8 -*-
from textwrap import dedent

from .nodeeditor.connection import Connection
from .nodeeditor.node import Node
from .nodeeditor.node_state import NodeState
from .utils.routinerecipe_error import RoutineRecipeError


def generate(start_node: Node) -> None:
    source: str = __generate(start_node)
    __write(source)


def __generate(start_node: Node) -> str:
    result: str = dedent('''\
        # -*- coding: utf-8 -*-
        from maya import cmds
        ''')
    result = __add_ln(result)
    result = __add_ln(result)
    result += 'def main():'
    result = __add_ln_indent(result)

    node_state: NodeState = start_node.state
    connections: list[Connection] = node_state.output_connections

    if not connections:
        raise RoutineRecipeError(u'Startノードに接続がありません')

    connection: Connection = connections[0]     # とりあえず決め打ちで1つ目だけ
    input_node: Node = connection.input_node
    result += input_node.source_code()
    result = __add_ln(result)
    return result


def __add_ln(source: str) -> str:
    return f'{source}\n'


def __add_ln_indent(source: str) -> str:
    return f'{source}\n    '


def __write(source: str):
    # TODO: パスの場所をちゃんと考える
    path = r'C:\Program Files\Autodesk\ApplicationPlugins\RoutineRecipe\Contents\scripts\routinerecipe\rr_main.py'
    with open(path, mode='w') as f:
        f.write(source)

    print(u'rr_main.pyを書き換えました')