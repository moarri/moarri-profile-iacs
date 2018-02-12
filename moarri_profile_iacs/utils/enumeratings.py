# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

from enum import Enum


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class CodeableEnum(Enum):

    def __init__(self, code):
        self.code = code

    @classmethod
    def value_of(cls, code):
        for e in list(cls):
            if e.code == code:
                return e
        return None