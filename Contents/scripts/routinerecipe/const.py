# -*- coding: utf-8 -*-
from .utils.readonly_meta import ReadonlyMeta


class Const(metaclass=ReadonlyMeta):
    TOOL_NAME: str = 'RoutineRecipe'

