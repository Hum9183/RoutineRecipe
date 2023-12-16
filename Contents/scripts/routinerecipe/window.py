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

from .run import run_recipe


class MyNodeData(NodeData):
    data_type = NodeDataType(id='MyNodeData', name='My Node Data')


class SimpleNodeData(NodeData):
    data_type = NodeDataType(id='SimpleData', name='Simple Data')


class NaiveDataModel(NodeDataModel):
    name = 'NaiveDataModel'
    caption = 'Caption'
    caption_visible = True
    num_ports = {
        PortType.input: 2,
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

class FlowData(NodeData):
    data_type = NodeDataType(id='FlowData', name='Flow')


class StringData(NodeData):
    data_type = NodeDataType(id='StringData', name='String')


class StartModel(NodeDataModel):
    name = 'StartModel'
    caption = 'Start'
    caption_visible = True
    num_ports = {
        PortType.input: 1,
        PortType.output: 1,
    }
    data_type = {
        PortType.input: {
            0: FlowData.data_type,
        },
        PortType.output: {
            0: FlowData.data_type,
        },
    }

    def out_data(self, port_index):
        return FlowData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        ...


class PrintModel(NodeDataModel):
    name = 'PrintModel'
    caption = 'Print'
    caption_visible = True
    num_ports = {
        PortType.input: 2,
        PortType.output: 2,
    }
    data_type = {
        PortType.input: {
            0: FlowData.data_type,
            1: StringData.data_type,
        },
        PortType.output: {
            0: FlowData.data_type,
            1: StringData.data_type,
        },
    }

    def out_data(self, port_index):
        return StringData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        ...

    def source_code(self) -> str:  # add
        return r'print("Hello World!!!!!!!!!!!!")'


def node_editor_main(app):
    registry = DataModelRegistry()
    registry.register_model(NaiveDataModel, category='My Category')
    registry.register_model(PrintModel, category='Maya')
    registry.register_model(StartModel, category='Maya')
    scene = FlowScene(registry=registry)

    connection_style = scene.style_collection.connection

    # Configure the style collection to use colors based on data types:
    connection_style.use_data_defined_colors = True

    view = FlowView(scene)
    view.resize(800, 600)

    start_node = scene.create_node(StartModel)
    print_node = scene.create_node(PrintModel)

    scene.create_connection(start_node[PortType.output][0],
                            print_node[PortType.input][0],
                            )

    return scene, view


class RoutineRecipeMainWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    instance_for_restore = None
    name = 'RoutineRecipe'
    title = 'Routine Recipe'

    def __init__(self, parent=None, *args, **kwargs):
        super(RoutineRecipeMainWindow, self).__init__(parent, *args, **kwargs)

    def init(self):
        self.setObjectName(RoutineRecipeMainWindow.name)
        self.setWindowTitle(RoutineRecipeMainWindow.title)

    def initGUI(self, node_editor_scene: FlowScene, node_editor_view: FlowView):
        self.setGeometry(500, 300, 400, 270)

        openMenu = QMenu("Open")
        openMenu.addAction("help")

        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+G")
        exitAction.triggered.connect(self.close)

        run_action = QAction('Run', self)
        run_action.setShortcut("Ctrl+R")
        run_action.triggered.connect(run_recipe)

        save_action = QAction('Save', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(lambda arg: node_editor_scene.save())

        load_action = QAction('Load', self)
        load_action.triggered.connect(lambda arg: node_editor_scene.load())

        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        fileMenu.addMenu(openMenu)
        fileMenu.addAction(exitAction)
        fileMenu.addAction(save_action)
        fileMenu.addAction(load_action)

        run_action = QAction('Run', self)
        run_action.triggered.connect(lambda arg: run_recipe(node_editor_scene))
        run_menu = menuBar.addMenu("Run")
        run_menu.addAction(run_action)


        self.setCentralWidget(node_editor_view)

def __create_window():
    app = QApplication.instance()
    # scene, view, nodes = node_editor_main(app)
    scene, view= node_editor_main(app)
    win = RoutineRecipeMainWindow()
    win.init()
    win.initGUI(scene, view)
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

def __restart_show_window():
    """開発用(リスタート用)"""
    cmds.deleteUI(RoutineRecipeMainWindow.name + 'WorkspaceControl', control=True)
    win = __create_window()
    cmd = dedent(
        """
        from routinerecipe import window
        import importlib
        importlib.reload(window)
        window.main_start(restore=True)
        """)
    win.show(dockable=True, uiScript=cmd)


def main_start(restore=False):
    if restore:
        __restore_window()
    else:
        __show_window()

def main_start_debug(restore=False):
    __restart_show_window()
