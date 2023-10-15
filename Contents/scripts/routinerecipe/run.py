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


def run_recipe():
    print('hello!!!!!!!!!')
