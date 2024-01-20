# -*- coding: utf-8 -*-
from PySide2.QtWidgets import QMainWindow, QMenu, QAction

from maya.app.general import mayaMixin

from . import restart_command
from .const import Const
from .nodeeditor.flow_scene import FlowScene
from .nodeeditor.flow_view import FlowView

from .run import run_recipe


class RoutineRecipeMainWindow(mayaMixin.MayaQWidgetDockableMixin, QMainWindow):
    restored_instance = None
    name = Const.TOOL_NAME
    title = Const.TOOL_TITLE
    workspace_control = f'{name}WorkspaceControl'

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

        restart_action = QAction('Restart', self)
        restart_action.triggered.connect(lambda *arg: restart_command.routine_recipe_restart_command())
        dev_menu = menuBar.addMenu("Dev")
        dev_menu.addAction(restart_action)

        self.setCentralWidget(node_editor_view)

# TODO:
# window closeのコールバックで
# cmds.deleteUI(RoutineRecipeMainWindow.name + 'WorkspaceControl', control=True)
# を実行する
