# -*- coding: utf-8 -*-
from textwrap import dedent

from maya import cmds


def __register_routinerecipe_startup():
    cmd = dedent(
        """
        import routinerecipe.startup
        routinerecipe.startup.execute()
        """)
    cmds.evalDeferred(cmd)


if __name__ == '__main__':
    try:
        __register_routinerecipe_startup()

    except Exception as e:
        import traceback
        traceback.print_exc()
