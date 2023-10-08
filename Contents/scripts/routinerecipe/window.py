# -*- coding: utf-8 -*-
from maya import cmds
from maya.common.ui import LayoutManager


class Window():
    def __init__(self, tool_name):
        """
        Args:
            tool_name (str): ツール名
        """
        self.tool_name = tool_name

    def show(self):
        """ウィンドウを生成し、表示する"""
        self.__delete_window()
        self._create_window()
        cmds.showWindow()

    def reload_window(self):
        """ウィンドウをリロードする。"""
        cmds.evalDeferred(lambda *args: self.show())

    def _create_window(self):
        cmds.window(self.tool_name, title=self.tool_name, menuBar=True, mxb=False, mnb=False)

    def __delete_window(self):
        """ウィンドウを削除する。"""
        if cmds.window(self.tool_name, ex=True):
            cmds.deleteUI(self.tool_name)
