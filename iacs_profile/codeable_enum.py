# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

from enum import Enum


class CodeableEnum(Enum):

    def __init__(self, code):
        self.code = code

    @classmethod
    def value_of(cls, code):
        for e in list(cls):
            if e.code == code:
                return e
        return None
