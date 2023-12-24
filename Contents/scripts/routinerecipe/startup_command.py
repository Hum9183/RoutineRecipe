# -*- coding: utf-8 -*-


def routine_recipe_startup_command():
    # WARNING: 現在、ここ経由だとreloadが正常に動作しない
    from routinerecipe import window, module_reloader
    module_reloader.deep_reload(window, 'routinerecipe')
    window.main_start()


if __name__ == '__main__':
    routine_recipe_startup_command()
