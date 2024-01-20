# -*- coding: utf-8 -*-
import _ast
import ast
import importlib
import inspect
import sys
from types import ModuleType
from typing import List, Any, Dict, Tuple, cast

# ref. https://graphics.hatenablog.com/entry/2019/12/22/052819

__package_name = ''


def deep_reload(module: ModuleType, package_name: str):
    global __package_name
    __package_name = package_name

    __delete_modules()

    from_import_symbols: List[Tuple[ModuleType, Dict[ModuleType, List[str]]]] = __get_symbols(module)

    parent: ModuleType
    children_symbols: Dict[ModuleType, List[str]]
    for parent, children_symbols in from_import_symbols:
        __reload(children_symbols)
        __overwrite_with_reloaded_symbols(parent, children_symbols)


def __delete_modules() -> None:
    global __package_name

    for module_name in list(sys.modules.keys()):
        if module_name.startswith(__package_name):
            del sys.modules[module_name]


def __get_symbols(parent: ModuleType) -> List[Tuple[ModuleType, Dict[ModuleType, List[str]]]]:
    children_symbols: Dict[ModuleType, List[str]] = get_children_symbols(parent)
    result = []
    for child_module in children_symbols.keys():
        result.extend(__get_symbols(child_module))
    result.append((parent, children_symbols))
    return result


def get_children_symbols(module: ModuleType):
    children_symbols: Dict[ModuleType, List[Any]] = {}

    source = inspect.getsource(module)

    tree: _ast.Module = ast.parse(source)

    stmt: _ast.stmt
    for stmt in tree.body:
        # TODO: import xxx の場合のサポートも必要？
        # from xxx import でないならcontinue
        if stmt.__class__ != _ast.ImportFrom:
            continue

        imp_frm = cast(_ast.ImportFrom, stmt)

        if imp_frm.module is None:
            # NOTE: from xxx import yyy のyyyがモジュールのため、シンボルを上書きするはない。
            continue

        module_name = imp_frm.module

        # モジュールのフルネームを取得
        if imp_frm.level == 0:
            module_full_name = f'{module_name}'
        elif imp_frm.level == 1:
            module_full_name = f'{module.__package__}.{module_name}'
        elif imp_frm.level >= 2:
            package_names = module.__package__.split('.')
            package_names = package_names[:-(imp_frm.level - 1)]
            package_names = '.'.join(package_names)
            module_full_name = f'{package_names}.{module_name}'
        else:
            raise Exception('module_reloaderにて例外が発生しました。ソースコードを確認してください')

        # リロード対象ではないならcontinue
        global __package_name
        if not module_full_name.startswith(__package_name):
            continue

        new_module: ModuleType = importlib.import_module(module_full_name)

        # packageならcontinue
        if __is_package(new_module):
            # NOTE: from xxx import yyy のyyyがモジュールのため、シンボルを上書きするはない。
            continue

        symbol_names: List[str] = [x.name for x in imp_frm.names]

        # wildcard importの場合
        if symbol_names[0] == '*':
            if '__all__' in new_module.__dict__:
                symbol_names = new_module.__dict__['__all__']
            else:
                symbol_names = [x for x in new_module.__dict__ if not x.startswith('__')]

        children_symbols[new_module] = symbol_names

    return children_symbols

    # TIPS: imp_frm.names[0].asnameでエイリアスを取得できる


def __is_package(module: ModuleType) -> bool:
    file = module.__file__
    return file is None or file.endswith('__init__.py')


def __reload(children_symbols: Dict[ModuleType, List[str]]) -> None:
    for child_module in children_symbols.keys():
        importlib.reload(child_module)


def __overwrite_with_reloaded_symbols(parent: ModuleType, children_symbols: Dict[ModuleType, List[str]]) -> None:
    no_key = 'no key'

    for child_module, child_symbol_names in children_symbols.items():
        for child_symbol_name in child_symbol_names:
            val = child_module.__dict__.get(child_symbol_name, no_key)
            if val == no_key:
                print(f'sys.modulesに{child_symbol_name}が存在しません')
            else:
                parent.__dict__[child_symbol_name] = val
