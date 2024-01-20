# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds
from maya import OpenMayaUI as omui

from PySide2.QtWidgets import QApplication, QWidget
import shiboken2

from . import restore_command
from .node_editor_setup import setup
from .window import RoutineRecipeMainWindow


def create_window() -> RoutineRecipeMainWindow:
    app = QApplication.instance()
    scene, view = setup(app)
    win = RoutineRecipeMainWindow()
    win.init()
    win.initGUI(scene, view)
    return win


def restore() -> None:
    RoutineRecipeMainWindow.restored_instance = create_window()    # WARNING: GCに破棄されないようにクラス変数に保存しておく
    ptr = omui.MQtUtil.findControl(RoutineRecipeMainWindow.name)
    restored_control = omui.MQtUtil.getCurrentParent()
    omui.MQtUtil.addWidgetToMayaLayout(int(ptr), int(restored_control))


def startup() -> None:
    ptr = omui.MQtUtil.findControl(RoutineRecipeMainWindow.name)

    if ptr:
        win = shiboken2.wrapInstance(int(ptr), QWidget)
        if win.isVisible():
            win.show()  # NOTE: show()することで再フォーカスする
        else:
            win.setVisible(True)
    else:
        win = create_window()
        cmd = dedent(inspect.getsource(restore_command))

        # 空のWindowが生成されてしまった場合
        if cmds.workspaceControl(RoutineRecipeMainWindow.workspace_control , q=True, exists=True):
            # 既存のWorkspaceControlを一旦削除する
            cmds.deleteUI(RoutineRecipeMainWindow.workspace_control, control=True)

        win.show(dockable=True, uiScript=cmd)


def restart() -> None:
    """開発用(再起動用)"""
    if omui.MQtUtil.findControl(RoutineRecipeMainWindow.name):
        cmds.deleteUI(RoutineRecipeMainWindow.workspace_control, control=True)

    win = create_window()
    cmd = dedent(inspect.getsource(restore_command))
    win.show(dockable=True, uiScript=cmd)