# -*- coding: utf-8 -*-
from textwrap import dedent

import importlib

from maya import cmds
from maya.common.ui import LayoutManager

import sys
import logging

from PySide2.QtWidgets \
    import QMainWindow, QMenu, QAction, QApplication, QWidget, QDockWidget
from PySide2 import QtWidgets
from PySide2 import QtCore
import shiboken2

from maya import OpenMayaUI as omui

from .nodeeditor.node_data import NodeData, NodeDataModel, NodeDataType
from .nodeeditor.data_model_registry import DataModelRegistry
from .nodeeditor.flow_scene import FlowScene
from .nodeeditor.flow_view import FlowView
from .nodeeditor.enums import PortType
from .nodeeditor.node import Node

from . import rr_main
from .nodeeditor.node_state import NodeState
from .nodeeditor.connection import Connection

from .utils.routinerecipe_error import RoutineRecipeError

# 実装案
# 1. 各NodeModelにPythonの実行テキストをもたせる(e.g. print())
# 2. start_nodeを起点に実装テキストを読み取っていく
# 3. 各Pythonの実装テキストを新規の.pyとして出力する(SourceGeneratorの要領)
# 4. 出力した.pyを実行する


@RoutineRecipeError.catch
def run_recipe(flow_scene: FlowScene):
    start_node: Node = __get_start_node(flow_scene, 'StartModel')
    source: str = __generate_source(start_node)
    __write(source)
    __run_rr_script()


def __generate_source(start_node: Node) -> str:
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

    if connections == []:
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
    path = r'C:\Program Files\Autodesk\ApplicationPlugins\RoutineRecipe\Contents\scripts\routinerecipe\rr_main.py'
    with open(path, mode='w') as f:
        f.write(source)
    print(u'rr_main.pyを書き換えました')


def __run_rr_script():
    importlib.reload(rr_main)
    rr_main.main()


def __get_start_node(flow_scene: FlowScene, expected_node_name: str) -> Node or None:
    nodes: dict = flow_scene.nodes  # TODO: TypedDictを検討
    for node in nodes.values():
        if node.model.name == expected_node_name:
            return node

    raise RoutineRecipeError(u'Startノードが存在しません')
