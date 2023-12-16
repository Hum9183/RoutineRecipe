# -*- coding: utf-8 -*-

def routine_recipe_startup_command():
    routine_recipe_reload_modules()
    routine_recipe_show_window()


def routine_recipe_reload_modules():
    from routinerecipe import window, run
    modules = [window, run]

    import importlib
    for m in modules:
        importlib.reload(m)

def routine_recipe_show_window():
    routine_recipe_reload_modules()

    from routinerecipe import window
    # import importlib
    # importlib.reload(window)

    # from routinerecipe.const import Const
    # wnd = Window(Const.TOOL_NAME)
    # wnd.show()

    window.main_start()

if __name__ == '__main__':
    routine_recipe_startup_command()
