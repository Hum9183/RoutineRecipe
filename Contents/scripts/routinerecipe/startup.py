# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds, mel

from .const import Const
from .main_commands import startup_command


def execute():
    mel.eval('''
    buildViewMenu MayaWindow|mainWindowMenu;
    setParent -menu "MayaWindow|mainWindowMenu";
    ''')

    cmds.menuItem(divider=True)

    startup_command_str = inspect.getsource(startup_command)
    cmds.menuItem(
        Const.TOOL_NAME,
        label=Const.TOOL_NAME,
        annotation='Run {}'.format(Const.TOOL_NAME),
        echoCommand=True,
        command=dedent(startup_command_str))
