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
        # from xxx import でないならcontinue
        if stmt.__class__ != _ast.ImportFrom:
            continue

        imp_frm = cast(_ast.ImportFrom, stmt)

        # モジュールのフルネームを取得
        # TODO: リファクタ
        if imp_frm.level == 1:
            module_full_name = f'{module.__package__}.{imp_frm.module}'
        elif imp_frm.level == 2:
            split: List[str] = module.__package__.split(".")[:-1]
            text = ".".join(split)
            module_full_name = f'{text}.{imp_frm.module}'
        # TODO: elif imp_frm.level == 3, 4, ...:
        else:
            module_full_name = imp_frm.module

        # Noneの場合
        # 未実装のため暫定的にcontinueする
        # TODO: Noneの場合に対応する
        # e.g. from . import extensions
        # e.g. from . import xxx
        if imp_frm.module is None:
            module_full_name = f'{module.__package__}.{imp_frm.names[0].name}'
            # tips: imp_frm.names[0].asnameでエイリアスを取得できる

        # リロード対象ではないならcontinue
        global __package_name
        if not module_full_name.startswith(__package_name):
            continue

        new_module: ModuleType = importlib.import_module(module_full_name)

        symbol_names: List[str] = [x.name for x in imp_frm.names]

        # wildcard importの場合
        if symbol_names[0] == '*':
            if '__all__' in new_module.__dict__:
                symbol_names = new_module.__dict__['__all__']
            else:
                symbol_names = [x for x in new_module.__dict__ if not x.startswith('__')]

        # FEATURE: as対応
        # FEATURE: from xxx import moduleのパターン対応
        # (現在はfrom xxx import class or function or ...にのみ対応)
        # (ちなみにmoduleの場合はシンボル上書きは必要ない？)

        # FEATURE: from xxx import module, module, ...のパターン対応

        children_symbols[new_module] = symbol_names

    return children_symbols


def __reload(children_symbols: Dict[ModuleType, List[str]]) -> None:
    for child_module in children_symbols.keys():
        importlib.reload(child_module)


def __overwrite_with_reloaded_symbols(parent: ModuleType, children_symbols: Dict[ModuleType, List[str]]) -> None:
    no_key = 'no key'

    for child_module, child_symbol_names in children_symbols.items():
        for child_symbol_name in child_symbol_names:
            val = child_module.__dict__.get(child_symbol_name, no_key)
            # from xxx import moduleやasに対応していないため、アドホック対応
            # TODO: ちゃんと実装する
            if val == no_key:
                print(f'sys.modulesに{child_symbol_name}が存在しません')
            else:
                parent.__dict__[child_symbol_name] = val
