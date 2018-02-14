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

import enum
from collections import namedtuple

from moarri_profile_iacs.profile_analysis.yellow_flags import YellowFlagsType
from moarri_profile_iacs.utils.enumeratings import AutoName, CodeableEnum


class DescriptionColumnType(AutoName):
    TESTS = enum.auto()
    YELLOW_FLAGS = enum.auto()
    HARDNESS = enum.auto()
    LWC = enum.auto()
    GRAIN_SIZE = enum.auto()
    GRAIN_SHAPE = enum.auto()
    DEPTH = enum.auto()
    SNOW_HEIGTH = enum.auto()
    DISTANCE = enum.auto()


class ColumnQualifier(AutoName):
    SINGLE = enum.auto()
    RIGHT = enum.auto()
    LEFT = enum.auto()
    MIDDLE = enum.auto()


_DESCRIPTION_COLUMN_NAMES = ['column_type', 'column_qualifier', 'present', 'label', 'width']

DescriptionColumn = namedtuple('DescriptionColumn', _DESCRIPTION_COLUMN_NAMES)

DEFAULT_COLUMN_SETTINGS = [
    DescriptionColumn(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.RIGHT, True, "", 30),
    DescriptionColumn(DescriptionColumnType.TESTS, ColumnQualifier.SINGLE, True, "Test", 50),
    DescriptionColumn(DescriptionColumnType.DISTANCE, ColumnQualifier.RIGHT, True, "", 25),
    DescriptionColumn(DescriptionColumnType.YELLOW_FLAGS, ColumnQualifier.SINGLE, True, "YF", 85),
    DescriptionColumn(DescriptionColumnType.GRAIN_SIZE, ColumnQualifier.SINGLE, True, "E", 50),
    DescriptionColumn(DescriptionColumnType.GRAIN_SHAPE, ColumnQualifier.SINGLE, True, "F", 40),
    DescriptionColumn(DescriptionColumnType.HARDNESS, ColumnQualifier.SINGLE, True, "", 30),
    DescriptionColumn(DescriptionColumnType.LWC, ColumnQualifier.SINGLE, True, "LWC", 30),
    DescriptionColumn(DescriptionColumnType.DISTANCE, ColumnQualifier.LEFT, True, "", 25),
    DescriptionColumn(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.MIDDLE, True, "", 29),
    DescriptionColumn(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.LEFT, True, "", 29)
]

_DRAWN_COLUMN_NAMES = ['column_type', 'column_qualifier', 'right_border', 'left_border', 'width', 'text_position']

DrawnColumn = namedtuple('DrawnColumn', _DRAWN_COLUMN_NAMES)


class YellowFlagsColumns(CodeableEnum):
    GRAIN_SIZE = (YellowFlagsType.GRAIN_SIZE)
    HARDNESS = (YellowFlagsType.HARDNESS)
    GRAIN_TYPE = (YellowFlagsType.GRAIN_TYPE)
    GRAIN_SIZE_DIFF = (YellowFlagsType.GRAIN_SIZE_DIFF)
    HARDNESS_DIFF = (YellowFlagsType.HARDNESS_DIFF)
    DEPTH = (YellowFlagsType.DEPTH)
    SUMMARY = (None)

    @staticmethod
    def find_column(yf_type):
        for yf in YellowFlagsColumns:
            if yf.code == yf_type:
                return yf
        return None


DEFAULT_YELLOW_FLAGS_NAMES = {
    YellowFlagsColumns.GRAIN_SIZE: 'S',
    YellowFlagsColumns.HARDNESS: 'H',
    YellowFlagsColumns.GRAIN_TYPE: 'T',
    YellowFlagsColumns.GRAIN_SIZE_DIFF: 'S',
    YellowFlagsColumns.HARDNESS_DIFF: 'H',
    YellowFlagsColumns.DEPTH: 'D',
    YellowFlagsColumns.SUMMARY: ''
}

_DRAWN_YELLOW_FLAGS_COLUMN_NAMES = _DRAWN_COLUMN_NAMES + ['borders', 'labels']


class DrawnYellowFlagsColumn(namedtuple('DrawnYellowFlagsColumn', _DRAWN_YELLOW_FLAGS_COLUMN_NAMES)):
    def __new__(cls, column_type, qualifier, right_border, left_border, width, text_position, main_markers_length,
                labels):
        detailed_flags_width = int((width - main_markers_length) / 7)
        text_shift = int(detailed_flags_width / 2)
        position = left_border
        brdrs = []
        lbls = {}
        for yfc in YellowFlagsColumns:
            if yfc != YellowFlagsColumns.SUMMARY:
                brdrs.append(position + detailed_flags_width)
                lbls[yfc] = (position + text_shift, labels[yfc])
                position += detailed_flags_width
            else:
                subcolumn_width = width - detailed_flags_width*6 - main_markers_length
                brdrs.append(position + subcolumn_width)
                lbls[yfc] = (int(position + subcolumn_width/2), labels[yfc])
                position += subcolumn_width

        self = super().__new__(cls, column_type, qualifier, right_border, left_border, width, text_position, brdrs,
                               lbls)
        return self


class DrawnColumns:
    def __init__(self):
        self._columns = []

    def add_column(self, c):
        self._columns.append(c)

    def last_column(self):
        return self._columns[-1] if len(self._columns) > 0 else None

    def first_column(self):
        return self._columns[0] if len(self._columns) > 0 else None

    def find_column_after(self, column_type, column_qualifier):
        pos = -1
        for i, col in enumerate(self._columns):
            if col.column_type == column_type and col.column_qualifier == column_qualifier:
                pos = i
                break
        return self._columns[pos + 1] if pos < len(self._columns) - 1 else None

    def find_column_before(self, column_type, column_qualifier):
        pos = -1
        for i, col in enumerate(self._columns):
            if col.column_type == column_type and col.column_qualifier == column_qualifier:
                pos = i
                break
        return self._columns[pos - 1] if pos > 0 else None

    def find_column(self, column_type, column_qualifier):
        for col in self._columns:
            if col.column_type == column_type and col.column_qualifier == column_qualifier:
                return col
        return None

    def find_single_column(self, column_type):
        return self.find_column(column_type, ColumnQualifier.SINGLE)

    def find_columns(self, column_type):
        return [col for col in self._columns if col.column_type == column_type]

    def last_column_border(self):
        return self._columns[-1].left_border if len(self._columns) > 0 else None
