# -*- coding: utf-8 -*-
from maya import cmds
from maya.common.ui import LayoutManager

import sys
import logging

from PySide2.QtWidgets \
    import QMainWindow, QMenu, QAction, QApplication
from PySide2 import QtWidgets

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


class MainWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, node_editor_view, parent=None, *args, **kwargs):
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        self.initUI(node_editor_view)

    def initUI(self, node_editor_view):
        self.setGeometry(500, 300, 400, 270)
        self.setWindowTitle('Routine Recipe')
        self.setObjectName('RoutineRecipe')

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

        ex = cmds.workspaceControl('Routine Recipe', q=True, exists=True)

        # print(ex)
        # self.close()


def main_start():
    test = omui.MQtUtil.findControl('RoutineRecipe')

    if test is not None:
        cmds.setFocus('RoutineRecipe')
        return
        # cmds.deleteUI('RoutineRecipe')
        # cmds.deleteUI('RoutineRecipe' + 'WorkspaceControl')

    logging.basicConfig(level='DEBUG')
    app = QApplication.instance()
    scene, view, nodes = node_editor_main(app)
    main_window = MainWindow(view)
    main_window.show(dockable=True)
    # print(main_window.showRepr())

    # topLevelWidgets = QApplication.topLevelWidgets()
    # for w in topLevelWidgets:
    #     print(w.objectName())
    #     print(w.windowTitle())
    #     if w.objectName() == 'RoutineRecipe':
    #         print('RoutineRecipeがすでに存在しているため、削除します')
    #         print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #         w.close()
    #         cmds.deleteUI('RoutineRecipe' + 'WorkspaceControl')

    sys.exit()
    app.exec_()

# TODO:
# - Mayaを起動しなおすとDockableが復元されない(https://qiita.com/sporty/items/a26ea7e4691437a6e8c8)
# - windowの出現位置を覚えさせる
