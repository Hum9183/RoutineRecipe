# -*- coding: utf-8 -*-
import importlib

def routine_recipe_startup_command():
    routine_recipe_reload_modules()
    routine_recipe_show_window()


def routine_recipe_reload_modules():
    from routinerecipe import source_generator, run, window
    modules = [source_generator, run, window]

    for m in modules:
        importlib.reload(m)


def routine_recipe_show_window():
    from routinerecipe import window
    window.main_start()


if __name__ == '__main__':
    routine_recipe_startup_command()
