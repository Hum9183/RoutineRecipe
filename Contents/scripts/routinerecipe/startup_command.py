# -*- coding: utf-8 -*-


def routine_recipe_startup_command():
    # WARNING:
    # startupコマンドではreloadは行わない。
    # 開発時は「Dev」=>「Restart」で再起動する(reloadされる)
    from routinerecipe import main
    main.startup()


if __name__ == '__main__':
    routine_recipe_startup_command()
