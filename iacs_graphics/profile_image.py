# -*- coding: utf-8 -*-


import os
import math
import enum
from iacs_graphics.tools import draw_centered_string
from utils.auto_enumerate import AutoName
from collections import namedtuple
from PIL import Image, ImageColor, ImageDraw, ImageFont
from iacs_profile.codeable_enum import CodeableEnum
from iacs_profile.iacs_caaml_types import IACSHardnessType
from iacs_graphics.enum_font_code import IACS_GRAIN_SHAPE_TYPE_DICT, IACS_HARDNESS_TYPE_DICT
from profile_analysis.yellow_flags import calculate_flags, YFValueType, YellowFlagsType

__author__ = 'Kuba Radliński'

SNOW_FONT_NAME = "IACSSnow"
SNOW_FONT_FILE_NAME = "IACSSnow.ttf"
DEFAULT_FONT_NAME = "arial.ttf"
DEFAULT_BOLD_FONT_NAME = "arialbd.ttf"


class _LayerDesc:
    y1 = 0
    y2 = 0
    thickness = 0
    layer = None

    def __init__(self, y1, y2, thickness, layer):
        self.y1 = y1
        self.y2 = y2
        self.thickness = thickness
        self.layer = layer


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

_DEFAULT_YELLOW_FLAGS_NAMES = {
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
    def __new__(cls, column_type, qualifier, right_border, left_border, width, text_position, main_markers_length, labels):
        detailed_flags_width = int((width -  main_markers_length) / 7)
        text_shift = int(detailed_flags_width / 2)
        position = left_border
        brdrs = []
        lbls = {}
        for yfc in YellowFlagsColumns:
            brdrs.append(position + detailed_flags_width)
            lbls[yfc] = (position + text_shift, labels[yfc])
            position += detailed_flags_width
        self = super().__new__(cls, column_type, qualifier, right_border, left_border, width, text_position, brdrs, lbls)
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


COLUMNS_4_CHECK = {
    'tests': ['yellow_flags', 'lwc', 'grain_size', 'grain_shape', 'hardness'],
    'yellow_flags': ['lwc', 'grain_size', 'grain_shape', 'hardness'],
    'lwc': ['grain_size', 'grain_shape', 'hardness'],
    'grain_size': ['grain_shape', 'hardness'],
    'grain_shape': ['hardness'],
    'hardness': []
}

DEFAULT_BORDER_SETTINGS = {
    'width': 2,
    'color': ImageColor.colormap['black']
}


class ProfileGraphicsImage:

    _snow_profile = None
    _graphics = None

    _page_width = 0
    _page_heigth = 0
    _top_x = 0
    _top_y = 0
    _width = 0
    _height = 0

    _snow_font = None
    _default_font = None
    _default_bold_font = None

    _border_width = 0
    _border_color = None

    _main_drawing_left_position = 0
    _main_drawing_right_position = 0

    _flags_character = "◄"

    _right_detailed_flags_position = 0

    temperatureUnitLabel = "-T[°C]"
    forceUnitLabel = "R[N]"
    font_size = 10
    snow_font_size = 12
    margin = 5

    columnborder_width = 1
    boottomOfGraph = 0
    maxSnowHeight = 100
    minTemp = -22
    temp_scale_height = 24
    hardnessScaleHeight = 24
    temp_unit_margin = 0
    tempHardnessSeparatorWidth = 1
    tempUnitMargin = 0
    forceUnitMargin = 0
    temp_text_vertical_position = 0
    hardnessTextVerticalPosition = 0
    temp_hardness_separator_position = 0
    main_left_position = 0
    main_right_position = 0
    bottomInnerPosition = 0
    hardnessTopPosition = 0
    bottomHarndesScalePosition = 0
    mainMarkersThicknes = 1
    mainMarkersLength = 4
    secondaryMarkersThicknes = 1
    secondaryMarkersLength = 2
    harndHardnessMarkersThicknes = 2
    handHardnessLineWidth = 2
    minimalLayerThickness = 18
    text_color = ImageColor.colormap['black']
    colorHandHardness = ImageColor.colormap['blue']
    opacityHandHardness = 60
    colorPitBaseSnow = ImageColor.colormap['lightgrey']
    colorGrid = ImageColor.colormap['grey']
    color_hand_harness_grid = ImageColor.colormap['black']
    colorTemp = ImageColor.colormap['red']
    colorBackground = ImageColor.colormap['white']
    color_flag = ImageColor.colormap['yellow']
    color_flag_total_score = ImageColor.colormap['red']
    temp_point_radius = 3
    graphSnowHeight = 0
    scaleVertical = 0
    scaleHorizontalHardness = 0
    scaleHorizontalTemp = 0

    def __init__(self, snow_profile, width, heigth, page_width=0, page_heigth=0, top_x=0, top_y=0):
        self._snow_profile = snow_profile
        self._width = width
        self._height = heigth
        self._page_width = page_width if page_width > 0 else width
        self._page_heigth = page_heigth if page_heigth > 0 else heigth
        self._top_x = top_x
        self._top_y = top_y
        self._yellow_flags = calculate_flags(snow_profile)
        self._column_settings = DEFAULT_COLUMN_SETTINGS.copy()
        self._border_settings = DEFAULT_BORDER_SETTINGS.copy()
        self._yellow_flags_names = _DEFAULT_YELLOW_FLAGS_NAMES.copy()
        self._draw_columns = DrawnColumns()

    def _init_fonts(self):
        self._snow_font = ImageFont.truetype(os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', SNOW_FONT_FILE_NAME)),
            size=self.snow_font_size)
        self._default_font = ImageFont.truetype(DEFAULT_FONT_NAME, size=self.font_size)
        self._default_bold_font = ImageFont.truetype(DEFAULT_BOLD_FONT_NAME, size=self.font_size)

    def _init_image(self):
        self.image = Image.new('RGB', (self._page_width, self._page_heigth), self.colorBackground)
        self._graphics = ImageDraw.Draw(self.image)
        self._border_color = self._border_settings['color']
        self._border_width = self._border_settings['width']

    def _draw_border(self):
        half_of_border = self._border_width / 2
        left_top = (self._top_x + half_of_border, self._top_y + half_of_border)
        right_top = (self._top_x + self._width - self._border_width, self._top_y + half_of_border)
        right_bottom = (self._top_x + self._width - self._border_width, self._top_y + self._height - half_of_border)
        left_bottom = (self._top_x + half_of_border, self._top_y + self._height - half_of_border)
        self._graphics.line([left_top, right_top], fill=self._border_color, width=self._border_width)
        self._graphics.line([right_top, right_bottom], fill=self._border_color, width=self._border_width)
        self._graphics.line([right_bottom, left_bottom], fill=self._border_color, width=self._border_width)
        self._graphics.line([left_bottom, left_top], fill=self._border_color, width=self._border_width)

    def _calculate_temp_hardness_separator_position(self):
        return

    def _check_next_columns(self, column_name):
        is_next = False
        for c in COLUMNS_4_CHECK[column_name]:
            is_next = is_next or self._column_settings[c].present
        return is_next

    def _prepare_main_drawing_area_values(self):
        self.main_left_position = self._top_x + self._border_width
        self.main_right_position = self._top_x + self._width - self._border_width - 1
        self.main_top_position = self._top_y + self._border_width
        self.temp_hardness_separator_position = self.main_top_position + self.temp_scale_height
        self.temp_text_vertical_position = self.main_left_position + int(
            (self.temp_scale_height - (self.tempHardnessSeparatorWidth / 2)) / 2)
        self.temp_unit_margin = self._graphics.textsize(self.temperatureUnitLabel)[0] + 3
        self.bottomInnerPosition = self._top_y + self._height - self._border_width - 1
        self.bottomHarndesScalePosition = self.main_top_position + self.temp_scale_height + self.hardnessScaleHeight
        self.hardnessTopPosition = self.bottomHarndesScalePosition + self.tempHardnessSeparatorWidth
        self.scaleVertical = (self.bottomInnerPosition - self.hardnessTopPosition) / (
                    self.maxSnowHeight - self.boottomOfGraph)
        self.hardnessTextVerticalPosition = self.main_top_position + self.temp_scale_height + int(
            self.tempHardnessSeparatorWidth / 2) + int((self.hardnessScaleHeight - self.tempHardnessSeparatorWidth) / 2)

    def _draw_inner_borders_scales_grids(self):
        self._graphics.line([self.main_left_position, self.bottomHarndesScalePosition, self._main_drawing_right_position,
                             self.bottomHarndesScalePosition], fill=self._border_color)
        self.forceUnitMargin = self._default_font.getsize(self.forceUnitLabel)[0] + 3
        draw_centered_string(self._graphics, (
        self.main_left_position + int(self.forceUnitMargin / 2), self.hardnessTextVerticalPosition),
                             self.forceUnitLabel,
                             self.text_color, self._default_font)
        self._graphics.line([self.main_left_position, self.temp_hardness_separator_position, self.main_right_position,
                             self.temp_hardness_separator_position], fill=self._border_color,
                            width=self.tempHardnessSeparatorWidth)
        draw_centered_string(self._graphics,
                             (self.main_left_position + (self.temp_unit_margin / 2), self.temp_text_vertical_position),
                             self.temperatureUnitLabel, self.text_color, self._default_font)

        self.scaleHorizontalTemp = (self._main_drawing_right_position - self.main_left_position) / abs(self.minTemp)
        shift = 2 if abs(self.minTemp) > 24 else 1
        for t in range(0, abs(self.minTemp), shift):
            x = self._main_drawing_right_position - int(t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength],
                                fill=self._border_color)
            topTempPosition = self.temp_hardness_separator_position - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength],
                                fill=self._border_color)
            label = str(t)
            labelWidth = self._default_font.getsize(label)[0]
            if (x + int(labelWidth / 2)) > (1 + self.main_left_position + self.temp_unit_margin):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color,
                                     self._default_font)
            if x > self._main_drawing_left_position and t > 0:
                self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)

        plusTempBorder = math.floor((self.main_right_position - self._main_drawing_right_position) / self.scaleHorizontalTemp)
        for t in range(0, plusTempBorder, shift):
            x = self._main_drawing_right_position + (t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength],
                                fill=self._border_color)
            topTempPosition = self.temp_hardness_separator_position - int(self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength],
                                fill=self._border_color)
            label = str(t)
            labelWidth = self._default_font.getsize(label)[0]
            if ((x + (labelWidth / 2)) < (1 + self.main_right_position)):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color,
                                     self._default_font)

        self.scaleHorizontalHardness = (self._main_drawing_right_position - self._main_drawing_left_position) / 1200
        for h in range(200, 1000, 200):

            x = self._main_drawing_right_position - int(h * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x,
                                 self.temp_hardness_separator_position + self.mainMarkersLength],
                                fill=self._border_color)
            topTempPosition = self.bottomHarndesScalePosition - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength],
                                fill=self._border_color)
            if h <= 1000:
                draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), str(h), self.text_color,
                                     self._default_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)

        hardnessPoints = [IACSHardnessType.F, IACSHardnessType.F4, IACSHardnessType.F1, IACSHardnessType.P,
                          IACSHardnessType.K, IACSHardnessType.I]
        for htype in hardnessPoints:
            x = self._main_drawing_right_position - (htype.hardness * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x,
                                 self.temp_hardness_separator_position + self.mainMarkersLength],
                                fill=self._border_color)
            topTempPosition = self.bottomHarndesScalePosition - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength],
                                fill=self._border_color)
            draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), htype.code, self.text_color,
                                 self._default_bold_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition],
                                fill=self.color_hand_harness_grid)

    def _draw_data_columns(self):
        top_columns_position = self.temp_hardness_separator_position + int(self.tempHardnessSeparatorWidth / 2)
        last_column_border = self.main_right_position

        for dc in self._column_settings:
            if dc.present:
                if dc.column_type == DescriptionColumnType.SNOW_HEIGTH and dc.column_qualifier == ColumnQualifier.LEFT:
                    leftPosition = self.main_left_position
                    rightPosition = leftPosition + dc.width
                    lastColumnBorder = leftPosition
                    textPosition = rightPosition - int((dc.width - self.columnborder_width) / 2)
                    if len(dc.label) > 0:
                        draw_centered_string(self._graphics, (textPosition, self.hardnessTextVerticalPosition),dc.label,
                                         self.text_color, self._default_font)
                    self._graphics.line(
                            [last_column_border, top_columns_position, last_column_border, self.bottomInnerPosition],
                            fill=self._border_color)
                    self._draw_columns.add_column(DrawnColumn(dc.column_type, dc.column_qualifier, rightPosition,
                                                                 leftPosition, dc.width, textPosition));

                else:
                    rightPosition = last_column_border
                    leftPosition = rightPosition - dc.width
                    last_column_border = leftPosition
                    textPosition = rightPosition - int((dc.width - self.columnborder_width) / 2)
                    if len(dc.label) > 0:
                        draw_centered_string(self._graphics, (textPosition, self.hardnessTextVerticalPosition), dc.label,
                                             self.text_color, self._default_font)
                    self._graphics.line(
                            [last_column_border, top_columns_position, last_column_border, self.bottomInnerPosition],
                            fill=self._border_color)
                    if dc.column_type == DescriptionColumnType.YELLOW_FLAGS:
                        drawn_column = DrawnYellowFlagsColumn(dc.column_type, dc.column_qualifier, rightPosition,
                                                              leftPosition, dc.width, textPosition,
                                                              self.mainMarkersLength, self._yellow_flags_names)
                        for b in drawn_column.borders[0:-1]:
                            self._graphics.line(
                                [b, self.hardnessTopPosition, b, self.bottomInnerPosition],
                                fill=self.colorGrid)
                        for yfc in YellowFlagsColumns:
                            lbl = drawn_column.labels[yfc]
                            if len(lbl[1]) > 0:
                                draw_centered_string(self._graphics, (lbl[0], self.hardnessTopPosition), lbl[1],
                                                     self.text_color, self._default_font)
                    else:
                        drawn_column = DrawnColumn(dc.column_type, dc.column_qualifier, rightPosition,
                                                                 leftPosition, dc.width, textPosition)
                    self._draw_columns.add_column(drawn_column)
        leftSnowHeightColumn = self._draw_columns.find_column(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.LEFT)
        self._main_drawing_left_position = leftSnowHeightColumn.right_border if leftSnowHeightColumn is not None else self.main_left_position
        self._main_drawing_right_position = self._draw_columns.find_column(DescriptionColumnType.SNOW_HEIGTH,
                                                                           ColumnQualifier.MIDDLE).left_border
        for dc in self._draw_columns.find_columns(DescriptionColumnType.SNOW_HEIGTH):
            self._draw_snow_heights(dc.left_border, dc.right_border,
                                    skip_last=(dc.column_qualifier == ColumnQualifier.LEFT))

    def _draw_snow_heights(self, left_position, rigth_position, skip_last=False):
        center_depth_position = left_position + int((rigth_position - left_position - self.columnborder_width) / 2)
        for sh in range(self.boottomOfGraph, self.maxSnowHeight + 10, 10):
            y = self.bottomInnerPosition - ((sh - self.boottomOfGraph) * self.scaleVertical)
            self._graphics.line([left_position, y, left_position + self.mainMarkersLength, y],
                                fill=self._border_color)
            self._graphics.line(
                [rigth_position, y, rigth_position - self.mainMarkersLength, y],
                fill=self._border_color)
            if sh > self.boottomOfGraph:
                write_label = True if not skip_last else sh < self.maxSnowHeight
                if write_label:
                    draw_centered_string(self._graphics, (center_depth_position, y), str(sh), self.text_color,
                                         self._default_font)
                for i in range(2, 10, 2):
                    y1 = self.bottomInnerPosition - ((sh - i - self.boottomOfGraph) * self.scaleVertical)
                    self._graphics.line(
                        [left_position, y1, left_position + self.secondaryMarkersLength, y1],
                        fill=self._border_color)
                    self._graphics.line([rigth_position, y1,
                                         rigth_position - self.secondaryMarkersLength, y1],
                                        fill=self._border_color)

    def _draw_temp_profile(self):
        if self._snow_profile is None:
            return
        temp_profile = self._snow_profile.results.measurements.temp_profile.temp_profile
        last = None
        top_height = self._snow_profile.results.measurements.hs.snow_height
        air_temp = self._snow_profile.results.measurements.air_temp_pres
        if air_temp is not None:
            last = (
            self._main_drawing_right_position + int(air_temp * self.scaleHorizontalTemp), self.temp_hardness_separator_position)
            self._graphics.ellipse(
                [last[0] - self.temp_point_radius, last[1] - self.temp_point_radius, last[0] + self.temp_point_radius,
                 last[1] + self.temp_point_radius], outline=self.colorTemp, fill=self.colorTemp)
        first_obs = True
        for obs in temp_profile:
            current = (self._main_drawing_right_position + int(obs.snow_temp * self.scaleHorizontalTemp),
                       self.bottomInnerPosition - int(
                           (top_height - obs.depth - self.boottomOfGraph) * self.scaleVertical))
            if first_obs:
                first_obs = False
                if last is not None:
                    # graphics.setStroke(airStroke)
                    self._graphics.line([last, current], fill=self.colorTemp, width=3)
            else:
                if last is not None:
                    self._graphics.line([last, current], fill=self.colorTemp, width=3)
            self._graphics.ellipse([current[0] - self.temp_point_radius, current[1] - self.temp_point_radius,
                                    current[0] + self.temp_point_radius, current[1] + self.temp_point_radius],
                                   outline=self.colorTemp, fill=self.colorTemp)
            last = current

    def _draw_layers(self):
        if self._snow_profile is None:
            return
        layers = self._snow_profile.results.measurements.strat_profile
        top_height = self._snow_profile.results.measurements.hs.snow_height
        first_layer = True
        layers_hardness = []
        last = None
        last_layer = None
        for l in layers:
            if first_layer:
                y = self.bottomInnerPosition - int((top_height - l.depth_top - self.boottomOfGraph) * self.scaleVertical)
                start = (self._main_drawing_right_position, y,)
                last = (self._main_drawing_right_position - int(l.hardness.cardinal_value.hardness * self.scaleHorizontalHardness), y,)
                layers_hardness.append(start)
                layers_hardness.append(last)
                first_layer = False
            else:
                if l.hardness.cardinal_value != last_layer.hardness.cardinal_value:
                    y = self.bottomInnerPosition - int(
                        (top_height - l.depth_top - self.boottomOfGraph) * self.scaleVertical)
                    p1 = (last[0], y,)
                    layers_hardness.append(p1)
                    last = (
                    self._main_drawing_right_position - int(l.hardness.cardinal_value.hardness * self.scaleHorizontalHardness),
                    y,)
                    layers_hardness.append(last)
            last_layer = l
        if last_layer is not None:
            y = self.bottomInnerPosition - int(
                (top_height - (last_layer.depth_top + last_layer.thickness) - self.boottomOfGraph) * self.scaleVertical)
            p1 = (last[0], y,)
            layers_hardness.append(p1)
            last = (self._main_drawing_right_position, y,)
            layers_hardness.append(last)
            # layersHardness.append(start)
            fill_color = ImageColor.getrgb(self.colorHandHardness)
            fill_color = (fill_color[0], fill_color[1], fill_color[2], self.opacityHandHardness)
            self._graphics.polygon(layers_hardness, fill=fill_color, outline=self.colorHandHardness)

            if last_layer.depth_top + last_layer.thickness > self.boottomOfGraph:
                y = last[1] + (self.handHardnessLineWidth / 2)
                # lineStroke = new BasicStroke(1)
                self._graphics.rectangle(
                    [self._main_drawing_left_position + 1, y, self._main_drawing_right_position, self.bottomInnerPosition],
                    fill=self.colorPitBaseSnow)

    def _create_layer_desc(self, l):
        th = int(l.thickness * self.scaleVertical)
        th = th if th >= self.minimalLayerThickness else self.minimalLayerThickness
        return _LayerDesc(0, 0, th, l)

    def _draw_layers_desc(self, adjust_2_now_top=True):
        if self._snow_profile is None:
            return
        layers = self._snow_profile.results.measurements.strat_profile
        top_height = self._snow_profile.results.measurements.hs.snow_height
        descs = [self._create_layer_desc(l) for l in layers]
        descs.append(_LayerDesc(0, 0, 0, None))
        desc_thickness = sum([d.thickness for d in descs])
        top_position = int((top_height - self.boottomOfGraph) * self.scaleVertical)
        top_position = desc_thickness if desc_thickness > top_position else top_position
        last = None
        for l in descs:
            if l.layer is not None:
                l.y1 = self.bottomInnerPosition - int(
                    (top_height - l.layer.depth_top - self.boottomOfGraph) * self.scaleVertical)
                l.y2 = self.bottomInnerPosition - top_position if last is None else last.y2 + last.thickness
            else:
                l.y1 = last.y1 + last.thickness
                l.y2 = last.y2 + last.thickness
            if l.y2 > l.y1 and last.thickness > self.minimalLayerThickness:
                possible_reduction = last.thickness - self.minimalLayerThickness
                difference = l.y2 - l.y1
                reduction = difference if possible_reduction > difference else possible_reduction
                l.y2 = l.y2 - reduction
                last.thickness = last.thickness - reduction
            last = l
        desc_thickness = sum([x.thickness for x in descs])
        if desc_thickness > (len(descs) - 1) * self.minimalLayerThickness:
            possible_reduction = sum(
                [(d.thickness - self.minimalLayerThickness) for d in descs if d.thickness > self.minimalLayerThickness])
            if descs[0].y2 < descs[0].y1:
                necesary_reduction = descs[0].y1 - descs[0].y2
                if adjust_2_now_top:
                    necesary_reduction = necesary_reduction if necesary_reduction <= possible_reduction else possible_reduction
                else:
                    text_gap = 3 * self._default_font.getsize("S")[1]
                    max_desc_position = self.hardnessTopPosition + text_gap
                    act_position = self.bottomInnerPosition - desc_thickness
                    necesary_reduction = max_desc_position - act_position
                while necesary_reduction > 0:
                    total_reduction = 0
                    for d in descs[-2::-1]:
                        if d.thickness > (self.minimalLayerThickness) and necesary_reduction > 0:
                            d.thickness -= 1
                            total_reduction += 1
                            necesary_reduction -= 1
                        d.y2 += total_reduction

        flag_pos = 0
        for l in descs:
            right_distance_column = self._draw_columns.find_column(DescriptionColumnType.DISTANCE, ColumnQualifier.RIGHT)
            left_distance_column = self._draw_columns.find_column(DescriptionColumnType.DISTANCE, ColumnQualifier.LEFT)
            left_left_distance_position = left_distance_column.left_border
            right_left_distance_position = left_distance_column.right_border
            left_rigth_distance_position = right_distance_column.left_border if right_distance_column else self.main_right_position
            right_rigth_distance_position = right_distance_column.right_border if right_distance_column else self.main_right_position
            self._graphics.line(
                [(left_left_distance_position, l.y1), (right_left_distance_position, l.y2)],
                fill=self._border_color, width=1)
            col = self._draw_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
            x = col.left_border if col and l.layer  and flag_pos > 0 else left_rigth_distance_position
            self._graphics.line([(right_left_distance_position, l.y2), (x, l.y2)], fill=self._border_color,
                                width=1)
            self._graphics.line(
                [(left_rigth_distance_position, l.y2), (right_rigth_distance_position, l.y1)],
                fill=self._border_color, width=1)

            col = self._draw_columns.find_column(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.LEFT)
            if col:
                x1 = col.right_border
                x2 = x1 + self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)

            col = self._draw_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
            if col:
                x1 = col.right_border
                x2 = x1 - self.mainMarkersLength
                self._graphics.line([(x1, l.y2), (x2, l.y2)], fill=self._border_color, width=1)
            col = self._draw_columns.find_single_column(DescriptionColumnType.TESTS)
            if col:
                x1 = col.left_border
                x2 = x1 + self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)
                x1 = col.right_border
                x2 = x2 - self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)

            textY = l.y2 + int(l.thickness / 2)
            if l.layer is not None:
                col = self._draw_columns.find_single_column(DescriptionColumnType.GRAIN_SIZE)
                if col:
                    avg = l.layer.grain_size.avg.double_value
                    avg_max = l.layer.grain_size.avg_max.double_value
                    text_avg = str(avg) if avg is not None and avg > 0.0 else ""
                    text_avg_max = str(avg_max) if avg_max is not None and avg_max > 0.0 else ""
                    txt = text_avg + " - " + text_avg_max
                    draw_centered_string(self._graphics, (col.text_position, textY), txt,
                                         self.text_color, self._default_font)
                col = self._draw_columns.find_single_column(DescriptionColumnType.GRAIN_SHAPE)
                if col:
                    txt = IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_primary]
                    if l.layer.grain_form_secondary is not None and l.layer.grain_form_secondary != l.layer.grain_form_primary:
                        txt = txt + IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_secondary]
                    draw_centered_string(self._graphics, (col.text_position, textY), txt,
                                         self.text_color,
                                         self._snow_font)
                col = self._draw_columns.find_single_column(DescriptionColumnType.HARDNESS)
                if col:
                    txt = IACS_HARDNESS_TYPE_DICT[l.layer.hardness.cardinal_value]
                    draw_centered_string(self._graphics, (col.text_position, textY), txt,
                                         self.text_color,
                                         self._snow_font)
                col = self._draw_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
                if col:
                    f = self._yellow_flags[flag_pos]
                    for flag in f.flags:
                        yfc = YellowFlagsColumns.find_column(flag)
                        if yfc:
                            lbl = col.labels[yfc]
                            if lbl:
                                draw_centered_string(self._graphics, (lbl[0], textY),
                                                     self._flags_character, self.color_flag, self._default_bold_font)
                    if flag_pos > 0:
                        f = self._yellow_flags[flag_pos - 1]
                        y = l.y2
                        for flag in f.flags:
                            yfc = YellowFlagsColumns.find_column(flag)
                            if yfc:
                                lbl = col.labels[yfc]
                                if lbl:
                                    draw_centered_string(self._graphics, (lbl[0], y),
                                                         self._flags_character, self.color_flag,
                                                         self._default_bold_font)
                            if f.layer_type() == YFValueType.LAYER_BOUNDARY and f.total_score > 0:
                                lbl = col.labels[YellowFlagsColumns.SUMMARY]
                                if lbl:
                                    draw_centered_string(self._graphics, (lbl[0], y), str(f.total_score),
                                                     self.color_flag_total_score, self._default_bold_font)
                    flag_pos += 2

    def draw_graph(self):
        self._init_fonts()
        self._init_image()
        self._draw_border()
        self._prepare_main_drawing_area_values()
        self._draw_data_columns()
        self._draw_inner_borders_scales_grids()
        self._draw_layers()
        self._draw_temp_profile()
        self._draw_layers_desc()
