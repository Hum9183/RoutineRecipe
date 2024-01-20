# -*- coding: utf-8 -*-


def routine_recipe_restart_command():
    from routinerecipe import main, const, module_reloader
    module_reloader.deep_reload(main, const.MODULE_NAME)
    main.restart()


if __name__ == '__main__':
    routine_recipe_restart_command()
