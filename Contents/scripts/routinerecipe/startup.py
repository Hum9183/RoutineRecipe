# -*- coding: utf-8 -*-
import inspect
from textwrap import dedent

from maya import cmds, mel

from .main_commands import startup_command


def execute():
    mel.eval('''
    buildViewMenu MayaWindow|mainWindowMenu;
    setParent -menu "MayaWindow|mainWindowMenu";
    ''')

    cmds.menuItem(divider=True)

    startup_command_str = inspect.getsource(startup_command)
    cmds.menuItem(
        'RoutineRecipe',
        label='RoutineRecipe',
        annotation='Run {}'.format('RoutineRecipe'),
        echoCommand=True,
        command=dedent(startup_command_str))
