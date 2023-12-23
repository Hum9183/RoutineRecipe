# -*- coding: utf-8 -*-
from maya import cmds

RR = "RoutineRecipe"


class Log:
    @staticmethod
    def log(message):
        print(u'{} : {}'.format(RR, message))

    @staticmethod
    def warning(message):
        cmds.warning(u'{} : {}'.format(RR, message))

    @staticmethod
    def error(message):
        cmds.error(u'{} : {}'.format(RR, message))