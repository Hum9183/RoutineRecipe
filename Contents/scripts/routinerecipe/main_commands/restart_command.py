# -*- coding: utf-8 -*-


def routine_recipe_restart_command():
    from routinerecipe import main, module_reloader
    module_reloader.deep_reload(main, 'routinerecipe')
    main.restart()


if __name__ == '__main__':
    routine_recipe_restart_command()
