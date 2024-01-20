# -*- coding: utf-8 -*-
import functools

from maya import cmds

from .log import Log


class RoutineRecipeError(Exception):
    @staticmethod
    def catch(function):
        """RoutineRecipeErrorを検知するデコレータ"""

        @functools.wraps(function)
        def wrapper(*args, **keywords):
            try:
                return_value = function(*args, **keywords)
            except RoutineRecipeError as e:
                e.log()
                return
            return return_value

        return wrapper

    def log(self):
        self.__output_scripteditor()
        self.__show_inviewmessage()

    def __output_scripteditor(self):
        msg = u'{}'.format(self)
        Log.log(msg)

    # TODO: RRWindow内に出したい
    def __show_inviewmessage(self):
        highlighted_msg = u'<hl>{}</hl>'.format(self)
        cmds.inViewMessage(amg=highlighted_msg, pos='botCenter', fade=True)
