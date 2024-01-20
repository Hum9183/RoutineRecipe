# -*- coding: utf-8 -*-


def routine_recipe_startup_command():
    # WARNING: reloadは行わない。開発時は開発用のコマンドを使用する。
    from routinerecipe import window
    window.startup()


if __name__ == '__main__':
    routine_recipe_startup_command()
