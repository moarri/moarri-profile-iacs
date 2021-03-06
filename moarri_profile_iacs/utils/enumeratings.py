# -*- coding: utf-8 -*-

# Copyright 2018 Moarri Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
