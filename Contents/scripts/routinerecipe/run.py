# -*- coding: utf-8 -*-
from textwrap import dedent

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

# 実装案
# 1. 各NodeModelにPythonの実行テキストをもたせる(e.g. print())
# 2. sceneのstateを頼りに、flow順でNodeを読み取っていく。
# 3. 各Pythonの実装テキストを新規の.pyとして出力する(SourceGeneratorの要領)
# 4. 出力した.pyを実行する
def run_recipe():
    print('hello!!!!!!!!!')
