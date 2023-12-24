# -*- coding: utf-8 -*-
import importlib

from .nodeeditor.flow_scene import FlowScene
from .nodeeditor.node import Node

from . import rr_main
from .utils.routinerecipe_error import RoutineRecipeError
from .source_generator import SourceGenerator

# 実装案
# 1. 各NodeModelにPythonの実行テキストをもたせる(e.g. print())
# 2. start_nodeを起点に実装テキストを読み取っていく
# 3. 各Pythonの実装テキストを新規の.pyとして出力する(SourceGeneratorの要領)
# 4. 出力した.pyを実行する


@RoutineRecipeError.catch
def run_recipe(flow_scene: FlowScene):
    start_node: Node = __get_start_node(flow_scene, 'StartModel')
    sg = SourceGenerator()
    sg.generate(start_node)
    __run_rr_script()


def __run_rr_script():
    importlib.reload(rr_main)
    rr_main.main()


def __get_start_node(flow_scene: FlowScene, expected_node_name: str) -> Node:
    nodes: dict = flow_scene.nodes  # TODO: TypedDictを検討
    for node in nodes.values():
        if node.model.name == expected_node_name:
            return node

    raise RoutineRecipeError(u'Startノードが存在しません')
