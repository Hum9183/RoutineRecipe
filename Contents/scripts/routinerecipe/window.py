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

from maya.app.general import mayaMixin

from maya import OpenMayaUI as omui

from .nodeeditor.node_data import NodeData, NodeDataModel, NodeDataType
from .nodeeditor.data_model_registry import DataModelRegistry
from .nodeeditor.flow_scene import FlowScene
from .nodeeditor.flow_view import FlowView
from .nodeeditor.enums import PortType


class MyNodeData(NodeData):
    data_type = NodeDataType(id='MyNodeData', name='My Node Data')


class SimpleNodeData(NodeData):
    data_type = NodeDataType(id='SimpleData', name='Simple Data')


class NaiveDataModel(NodeDataModel):
    name = 'NaiveDataModel'
    caption = 'Caption'
    caption_visible = True
    num_ports = {PortType.input: 2,
                 PortType.output: 2,
                 }
    data_type = {
        PortType.input: {
            0: MyNodeData.data_type,
            1: SimpleNodeData.data_type
        },
        PortType.output: {
            0: MyNodeData.data_type,
            1: SimpleNodeData.data_type
        },
    }

    def out_data(self, port_index):
        if port_index == 0:
            return MyNodeData()
        elif port_index == 1:
            return SimpleNodeData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        ...


def node_editor_main(app):
    registry = DataModelRegistry()
    registry.register_model(NaiveDataModel, category='My Category')
    scene = FlowScene(registry=registry)

    connection_style = scene.style_collection.connection

    # Configure the style collection to use colors based on data types:
    connection_style.use_data_defined_colors = True

    view = FlowView(scene)
    # view.setWindowTitle("Connection (data-defined) color example")
    view.resize(800, 600)

    node_a = scene.create_node(NaiveDataModel)
    node_b = scene.create_node(NaiveDataModel)

    scene.create_connection(node_a[PortType.output][0],
                            node_b[PortType.input][0],
                            )

    scene.create_connection(node_a[PortType.output][1],
                            node_b[PortType.input][1],
                            )

    return scene, view, [node_a, node_b]

class RoutineRecipeMainWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    instance_for_restore = None
    name = 'RoutineRecipe'
    title = 'Routine Recipe'

    def __init__(self, parent=None, *args, **kwargs):
        super(RoutineRecipeMainWindow, self).__init__(parent, *args, **kwargs)

    def init(self):
        self.setObjectName(RoutineRecipeMainWindow.name)
        self.setWindowTitle(RoutineRecipeMainWindow.title)

    def initGUI(self, node_editor_view):
        self.setGeometry(500, 300, 400, 270)

        openMenu = QMenu("Open")
        openMenu.addAction("help")

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+G")
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        fileMenu.addMenu(openMenu)
        fileMenu.addAction(exitAction)

        self.setCentralWidget(node_editor_view)

def __create_window():
    app = QApplication.instance()
    scene, view, nodes = node_editor_main(app)
    win = RoutineRecipeMainWindow()
    win.init()
    win.initGUI(view)
    return win

def __restore_window():
    RoutineRecipeMainWindow.instance_for_restore = __create_window() # WARNING: GCに破棄されないようにクラス変数に保存しておく
    # Add custom mixin widget to the workspace control
    mixin_ptr = omui.MQtUtil.findControl(RoutineRecipeMainWindow.name)
    # Grab the created workspace control with the following.
    restored_control = omui.MQtUtil.getCurrentParent()
    omui.MQtUtil.addWidgetToMayaLayout(int(mixin_ptr), int(restored_control))

def __show_window():
    ''' When the control is restoring, the workspace control has already been created and
        all that needs to be done is restoring its UI.
    '''
    ptr = omui.MQtUtil.findControl(RoutineRecipeMainWindow.name)

    if ptr:
        win = shiboken2.wrapInstance(int(ptr), QWidget)
        if win.isVisible():
            win.show() # NOTE: show()することで再フォーカスする
        else:
            win.setVisible(True)
    else:
        # Create a custom mixin widget for the first time
        win = __create_window()

        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        # customMixinWindow.show(dockable=True, height=600, width=480, uiScript='DockableWidgetUIScript(restore=True)')
        cmd = dedent(
            """
            from routinerecipe import window
            import importlib
            importlib.reload(window)
            window.main_start(restore=True)
            """)
        win.show(dockable=True, uiScript=cmd)

    return win


def main_start(restore=False):
    if restore:
        __restore_window()
    else:
        __show_window()
