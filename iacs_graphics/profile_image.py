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

    def __init__(self, y1, y2, thickness,  layer):
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


_DESCRIPTION_COLUMN_NAMES = ['type', 'qualifier', 'present', 'label', 'width']

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


_DRAWN_COLUMN_NAMES = ['type', 'qualifier', 'right_border', 'left_border', 'width', 'text_position']

DrawnColumn = namedtuple('DrawnColumn', _DRAWN_COLUMN_NAMES)


class YellowFlagsColumns(CodeableEnum):
    GRAIN_SIZE = (YellowFlagsType.GRAIN_SIZE)
    HARDNESS = (YellowFlagsType.HARDNESS)
    GRAIN_TYPE = (YellowFlagsType.GRAIN_TYPE)
    GRAIN_SIZE_DIFF = (YellowFlagsType.GRAIN_SIZE_DIFF)
    HARDNESS_DIFF = (YellowFlagsType.HARDNESS_DIFF)
    DEPTH = (YellowFlagsType.DEPTH)
    SUMMARY = (None)


_DRAWN_YF_COLUMN_NAMES = _DRAWN_COLUMN_NAMES.extend(['borders', 'label_positions'])


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

    _column_settings = DEFAULT_COLUMN_SETTINGS.copy()
    _border_settings = DEFAULT_BORDER_SETTINGS.copy()

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

    _separator_width = 15
    _left_separator_position_left = 0
    _left_separator_position_right = 0

    _right_separator_position_left = 0
    _right_separator_position_right = 0

    _center_depth_position_left = 0
    _right_depth_position_left = 0
    _left_depth_position_right = 0

    _horizontal_test_position = 0
    _horizontal_yflags_position = 0
    _horizontal_lwc_position = 0
    _horizontal_hardness_position = 0
    _horizontal_grain_size_position = 0
    _horizontal_grain_shape_position = 0

    _left_flags_position = 0
    _flags_position_layer_grain_size = 0
    _flags_position_layer_hardness = 0
    _flags_position_layer_grain_type = 0

    _flags_position_boundary_grain_size_diff = 0
    _flags_position_boundary_hardness_diff = 0
    _flags_position_boundary_depth = 0

    _flags_position_total_score = 0

    _flags_layer_grain_size_label = "S"
    _flags_layer_hardness_label = "H"
    _flags_layer_grain_type_label = "T"

    _flags_boundary_grain_size_diff_label = "S"
    _flags_boundary_hardness_diff_label = "H"
    _flags_boundary_depth_label = "D"

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
    hardnessRightPosition = 0
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

    def _draw_column(self, column, horizontal_position, last_column_border, topColumnsPosition, label_vertical_position):
        if column.present:
            new_horizontal_position = last_column_border - (column.width - self.columnborder_width) / 2
            new_last_column_border = last_column_border-column.width
            if self._check_next_columns(column.column_name):
                self._graphics.line([new_last_column_border, topColumnsPosition, new_last_column_border, self.bottomInnerPosition], fill=self._border_color)
            if len(column.label) > 0:
                draw_centered_string(self._graphics, (new_horizontal_position, label_vertical_position), column.label,
                                          self.text_color, self._default_font)
            return new_horizontal_position, new_last_column_border
        else:
            return horizontal_position, last_column_border

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
        self.scaleVertical = (self.bottomInnerPosition - self.hardnessTopPosition) / (self.maxSnowHeight - self.boottomOfGraph)
        self.hardnessTextVerticalPosition = self.main_top_position + self.temp_scale_height + int(
            self.tempHardnessSeparatorWidth / 2) + int((self.hardnessScaleHeight - self.tempHardnessSeparatorWidth) / 2)

    def _draw_inner_borders_scales_grids(self):
        self._graphics.line([self.main_left_position, self.bottomHarndesScalePosition, self.hardnessRightPosition, self.bottomHarndesScalePosition], fill=self._border_color)
        self.forceUnitMargin = self._default_font.getsize(self.forceUnitLabel)[0] + 3
        draw_centered_string(self._graphics, (self.main_left_position + int(self.forceUnitMargin / 2), self.hardnessTextVerticalPosition), self.forceUnitLabel,
                                  self.text_color, self._default_font)
        self._graphics.line([self.main_left_position, self.temp_hardness_separator_position, self.main_right_position,
                             self.temp_hardness_separator_position], fill=self._border_color,
                            width=self.tempHardnessSeparatorWidth)
        draw_centered_string(self._graphics, (self.main_left_position + (self.temp_unit_margin / 2), self.temp_text_vertical_position),
                                  self.temperatureUnitLabel, self.text_color, self._default_font)



        self.scaleHorizontalTemp = (self.hardnessRightPosition - self.main_left_position) / abs(self.minTemp)
        shift = 2 if abs(self.minTemp) > 24 else 1
        for t in range(0, abs(self.minTemp), shift):
            x = self.hardnessRightPosition - int(t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength], fill=self._border_color)
            topTempPosition = self.temp_hardness_separator_position - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength], fill=self._border_color)
            label = str(t)
            labelWidth = self._default_font.getsize(label)[0]
            if (x + int(labelWidth / 2)) > (1 + self.main_left_position + self.temp_unit_margin):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color, self._default_font)
            if x > self._left_depth_position_right and t > 0:
                self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)

        plusTempBorder = math.floor((self.main_right_position - self.hardnessRightPosition) / self.scaleHorizontalTemp)
        for t in range(0, plusTempBorder, shift):
            x = self.hardnessRightPosition + (t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength], fill=self._border_color)
            topTempPosition = self.temp_hardness_separator_position - int(self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength], fill=self._border_color)
            label = str(t)
            labelWidth = self._default_font.getsize(label)[0]
            if ((x + (labelWidth / 2)) < (1 + self.main_right_position)):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color, self._default_font)

        self.scaleHorizontalHardness = (self.hardnessRightPosition - self._left_depth_position_right) / 1200
        for h in range(200, 1000, 200):

            x = self.hardnessRightPosition - int(h * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x, self.temp_hardness_separator_position + self.mainMarkersLength], fill=self._border_color)
            topTempPosition = self.bottomHarndesScalePosition - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength], fill=self._border_color)
            if h <= 1000:
                draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), str(h), self.text_color, self._default_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)

        hardnessPoints = [IACSHardnessType.F, IACSHardnessType.F4, IACSHardnessType.F1, IACSHardnessType.P, IACSHardnessType.K, IACSHardnessType.I]
        for htype in hardnessPoints:
            x = self.hardnessRightPosition - (htype.hardness * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x, self.temp_hardness_separator_position + self.mainMarkersLength], fill=self._border_color)
            topTempPosition = self.bottomHarndesScalePosition - (self.tempHardnessSeparatorWidth / 2)
            self._graphics.line([x, topTempPosition, x, topTempPosition - self.mainMarkersLength], fill=self._border_color)
            draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), htype.code, self.text_color, self._default_bold_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.color_hand_harness_grid)

    def _draw_data_columns(self):
        top_columns_position = self.temp_hardness_separator_position + int(self.tempHardnessSeparatorWidth / 2)
        last_column_border = self.main_right_position
        self._right_depth_position_left = last_column_border - self._column_settings['depth'].width
        self._graphics.line([self._right_depth_position_left, top_columns_position, self._right_depth_position_left,
                             self.bottomInnerPosition], fill=self._border_color)
        self._draw_snow_heights(self._right_depth_position_left, last_column_border)
        last_column_border = self._right_depth_position_left
        self._horizontal_test_position, last_column_border = self._draw_column(self._column_settings['tests'],
                                                                               self._horizontal_test_position,
                                                                               last_column_border, top_columns_position,
                                                                               self.hardnessTextVerticalPosition)
        self._right_separator_position_right = last_column_border
        self._right_separator_position_left = self._right_separator_position_right - self._separator_width
        # self._graphics.line(
        #     [self._right_separator_position_left, top_columns_position, self._right_separator_position_left,
        #      self.bottomInnerPosition], fill=self._border_color)
        # To poniżej to chyba strzał
        # self._graphics.line(
        #     [self._left_separator_position_left, top_columns_position, self._left_separator_position_left,
        #      self.bottomInnerPosition], fill=self._border_color)
        last_column_border = self._right_separator_position_left
        self._horizontal_yflags_position, last_column_border = self._draw_column(self._column_settings['yellow_flags'],
                                                                                 self._horizontal_yflags_position,
                                                                                 last_column_border,
                                                                                 top_columns_position,
                                                                                 self.hardnessTextVerticalPosition)
        self._left_flags_position = last_column_border
        self._horizontal_lwc_position, last_column_border = self._draw_column(self._column_settings['lwc'],
                                                                              self._horizontal_lwc_position,
                                                                              last_column_border, top_columns_position,
                                                                              self.hardnessTextVerticalPosition)
        self._horizontal_grain_size_position, last_column_border = self._draw_column(
            self._column_settings['grain_size'], self._horizontal_grain_size_position, last_column_border,
            top_columns_position, self.hardnessTextVerticalPosition)
        self._horizontal_grain_shape_position, last_column_border = self._draw_column(
            self._column_settings['grain_shape'], self._horizontal_grain_shape_position, last_column_border,
            top_columns_position, self.hardnessTextVerticalPosition)
        self._horizontal_hardness_position, last_column_border = self._draw_column(self._column_settings['hardness'],
                                                                                   self._horizontal_hardness_position,
                                                                                   last_column_border,
                                                                                   top_columns_position,
                                                                                   self.hardnessTextVerticalPosition)
        self._left_separator_position_right = last_column_border
        self._left_separator_position_left = self._left_separator_position_right - self._separator_width
        self._graphics.line(
            [self._left_separator_position_left, top_columns_position, self._left_separator_position_left,
             self.bottomInnerPosition], fill=self._border_color)
        self._center_depth_position_left = self._left_separator_position_left - self._column_settings['depth'].width
        self._graphics.line([self._center_depth_position_left, top_columns_position, self._center_depth_position_left,
                             self.bottomInnerPosition], fill=self._border_color)
        self._draw_snow_heights(self._center_depth_position_left, self._left_separator_position_left)
        self.hardnessRightPosition = self._center_depth_position_left - int(self.columnborder_width / 2)
        self._left_depth_position_right = self.main_left_position + self._column_settings['depth'].width
        self._graphics.line([self._left_depth_position_right, self.hardnessTopPosition, self._left_depth_position_right,
                             self.bottomInnerPosition], fill=self._border_color)
        self._draw_snow_heights(self.main_left_position, self._left_depth_position_right, skip_last=True)
        self._draw_yellow_flags_columns()

    def _draw_yellow_flags_columns(self):
        if self._column_settings['yellow_flags'].present:
            detailed_flags_width = int((self._column_settings['yellow_flags'].width - 2 * self.mainMarkersLength) / 8)
            text_shift = int(detailed_flags_width / 2)
            flags_start_position = self._left_flags_position + self.mainMarkersLength
            line_position = flags_start_position
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)

            self._flags_position_layer_grain_size = flags_start_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_layer_grain_size, self.hardnessTopPosition),
                                      self._flags_layer_grain_size_label, self.text_color, self._default_font)

            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)

            self._flags_position_layer_hardness = line_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_layer_hardness, self.hardnessTopPosition),
                                      self._flags_layer_hardness_label, self.text_color, self._default_font)
            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)

            self._flags_position_layer_grain_type = line_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_layer_grain_type, self.hardnessTopPosition),
                                      self._flags_layer_grain_type_label, self.text_color, self._default_font)
            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)
            self._right_detailed_flags_position = line_position

            self._flags_position_boundary_grain_size_diff = line_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_boundary_grain_size_diff, self.hardnessTopPosition),
                                      self._flags_boundary_grain_size_diff_label, self.text_color, self._default_font)
            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)

            self._flags_position_boundary_hardness_diff = line_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_boundary_hardness_diff, self.hardnessTopPosition),
                                      self._flags_boundary_hardness_diff_label, self.text_color, self._default_font)
            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)

            self._flags_position_boundary_depth = line_position + text_shift
            draw_centered_string(self._graphics, (self._flags_position_boundary_depth, self.hardnessTopPosition),
                                      self._flags_boundary_depth_label, self.text_color, self._default_font)
            line_position += detailed_flags_width
            self._graphics.line([line_position, self.hardnessTopPosition, line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)
            end_line_position = self._right_separator_position_left-self.mainMarkersLength
            self._graphics.line([end_line_position, self.hardnessTopPosition, end_line_position, self.bottomInnerPosition],
                                fill=self.colorGrid)
            self._flags_position_total_score = line_position + int((end_line_position-line_position)/2)


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
        tempProfile = self._snow_profile.results.measurements.temp_profile.temp_profile
        last = None
        topHeight = self._snow_profile.results.measurements.hs.snow_height
        airTemp = self._snow_profile.results.measurements.air_temp_pres
        if airTemp is not None:
            last = (self.hardnessRightPosition + int(airTemp * self.scaleHorizontalTemp), self.temp_hardness_separator_position)
            self._graphics.ellipse([last[0] - self.temp_point_radius, last[1] - self.temp_point_radius, last[0] + self.temp_point_radius, last[1] + self.temp_point_radius], outline=self.colorTemp, fill=self.colorTemp)
        firstObs = True
        for obs in tempProfile:
            current = (self.hardnessRightPosition + int(obs.snow_temp * self.scaleHorizontalTemp), self.bottomInnerPosition - int((topHeight - obs.depth - self.boottomOfGraph) * self.scaleVertical))
            if firstObs:
                firstObs = False
                if last is not None:
                    # graphics.setStroke(airStroke)
                    self._graphics.line([last, current], fill=self.colorTemp, width=3)
            else:
                if last is not None:
                    self._graphics.line([last, current], fill=self.colorTemp, width=3)
            self._graphics.ellipse([current[0] - self.temp_point_radius, current[1] - self.temp_point_radius, current[0] + self.temp_point_radius, current[1] + self.temp_point_radius], outline=self.colorTemp, fill=self.colorTemp)
            last = current

    def _draw_layers(self):
        if self._snow_profile is None:
            return
        layers = self._snow_profile.results.measurements.strat_profile
        topHeight = self._snow_profile.results.measurements.hs.snow_height
        firstLayer = True
        layersHardness = []
        start = None
        last = None
        lastLayer = None
        for l in layers:
            if firstLayer:
                y = self.bottomInnerPosition - int((topHeight - l.depth_top - self.boottomOfGraph) * self.scaleVertical)
                start = (self.hardnessRightPosition, y,)
                last = (self.hardnessRightPosition - int(l.hardness.cardinal_value.hardness * self.scaleHorizontalHardness), y,)
                layersHardness.append(start)
                layersHardness.append(last)
                firstLayer = False
            else:
                if l.hardness.cardinal_value != lastLayer.hardness.cardinal_value:
                    y = self.bottomInnerPosition - int((topHeight - l.depth_top - self.boottomOfGraph) * self.scaleVertical)
                    p1 = (last[0], y,)
                    layersHardness.append(p1)
                    last = (self.hardnessRightPosition - int(l.hardness.cardinal_value.hardness * self.scaleHorizontalHardness), y,)
                    layersHardness.append(last)
            lastLayer = l
        if lastLayer is not None:
            y = self.bottomInnerPosition - int((topHeight - (lastLayer.depth_top + lastLayer.thickness) - self.boottomOfGraph) * self.scaleVertical)
            p1 = (last[0], y,)
            layersHardness.append(p1)
            last = (self.hardnessRightPosition, y,)
            layersHardness.append(last)
            # layersHardness.append(start)
            fill_color = ImageColor.getrgb(self.colorHandHardness)
            fill_color = (fill_color[0], fill_color[1], fill_color[2], 0)
            self._graphics.polygon(layersHardness, fill=fill_color, outline=self.colorHandHardness)

            if lastLayer.depth_top + lastLayer.thickness > self.boottomOfGraph:
                y = last[1] + (self.handHardnessLineWidth / 2)
                # lineStroke = new BasicStroke(1)
                self._graphics.rectangle([self._left_depth_position_right+1, y, self.hardnessRightPosition, self.bottomInnerPosition], fill=self.colorPitBaseSnow)

    def _create_layer_desc(self,l):
        th = int(l.thickness * self.scaleVertical)
        th = th if th >= self.minimalLayerThickness else self.minimalLayerThickness
        return _LayerDesc(0,0, th, l)

    def _draw_layers_desc(self, adjust_2_now_top=True):
        if self._snow_profile is None:
            return
        layers = self._snow_profile.results.measurements.strat_profile
        topHeight = self._snow_profile.results.measurements.hs.snow_height
        descs = [self._create_layer_desc(l) for l in layers]
        descs.append(_LayerDesc(0,0, 0, None))
        descThickness = sum([d.thickness for d in descs])
        topPosition = int((topHeight - self.boottomOfGraph) * self.scaleVertical)
        topPosition = descThickness if descThickness > topPosition else topPosition
        last = None
        for l in descs:
            if l.layer is not None:
                l.y1 = self.bottomInnerPosition - int((topHeight - l.layer.depth_top - self.boottomOfGraph) * self.scaleVertical)
                l.y2 = self.bottomInnerPosition - topPosition if last is None else last.y2 + last.thickness
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
        descThickness = sum([x.thickness for x in descs])
        if descThickness > (len(descs)-1) * self.minimalLayerThickness:
            possible_reduction = sum([(d.thickness - self.minimalLayerThickness) for d in descs if d.thickness > self.minimalLayerThickness])
            if descs[0].y2 < descs[0].y1:
                necesary_reduction = descs[0].y1 - descs[0].y2
                if adjust_2_now_top:
                    necesary_reduction = necesary_reduction if necesary_reduction <= possible_reduction else possible_reduction
                else:
                    text_gap = 3 * self._default_font.getsize("S")[1]
                    max_desc_position = self.hardnessTopPosition + text_gap
                    act_position = self.bottomInnerPosition - descThickness
                    necesary_reduction =  max_desc_position - act_position
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
            self._graphics.line([(self._left_separator_position_left, l.y1), (self._left_separator_position_right, l.y2)], fill=self._border_color, width=1)
            x = self._right_detailed_flags_position if self._column_settings['yellow_flags'].present and l.layer is not None and flag_pos > 0 else self._right_separator_position_left
            self._graphics.line([(self._left_separator_position_right, l.y2), (x, l.y2)], fill=self._border_color,
                                width=1)
            self._graphics.line([(self._right_separator_position_left, l.y2), (self._right_separator_position_right, l.y1)], fill=self._border_color, width=1)

            x1 = self._left_depth_position_right
            x2 = self._left_depth_position_right + self.mainMarkersLength
            self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)

            if self._column_settings['yellow_flags'].present:
                x1 = self._right_separator_position_left
                x2 = self._right_separator_position_left-self.mainMarkersLength
                self._graphics.line([(x1, l.y2), (x2, l.y2)], fill=self._border_color, width=1)
            if self._column_settings['tests'].present:
                x1 = self._right_separator_position_right
                x2 = self._right_separator_position_right + self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)
                x1 = self._right_depth_position_left
                x2 = self._right_depth_position_left - self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=self._border_color, width=1)

            textY = l.y2 + int(l.thickness / 2)
            if l.layer is not None:
                if self._column_settings['grain_size'].present:
                    avg = l.layer.grain_size.avg.double_value
                    avg_max = l.layer.grain_size.avg_max.double_value
                    text_avg = str(avg) if avg is not None and avg > 0.0 else ""
                    text_avg_max = str(avg_max) if avg_max is not None and avg_max > 0.0 else ""
                    txt = text_avg + " - " + text_avg_max
                    draw_centered_string(self._graphics, (self._horizontal_grain_size_position, textY), txt, self.text_color, self._default_font)
                if self._column_settings['grain_shape'].present:
                    txt = IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_primary]
                    if l.layer.grain_form_secondary is not None and l.layer.grain_form_secondary != l.layer.grain_form_primary:
                        txt = txt + IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_secondary]
                    draw_centered_string(self._graphics, (self._horizontal_grain_shape_position, textY), txt, self.text_color,
                                              self._snow_font)
                if self._column_settings['hardness'].present:
                    txt = IACS_HARDNESS_TYPE_DICT[l.layer.hardness.cardinal_value]
                    draw_centered_string(self._graphics, (self._horizontal_hardness_position, textY), txt, self.text_color,
                                              self._snow_font)
                f = self._yellow_flags[flag_pos]
                if f.type() == YFValueType.LAYER:

                    if f.av_grain_size:
                        draw_centered_string(self._graphics, (self._flags_position_layer_grain_size, textY), self._flags_character, self.color_flag, self._default_bold_font)

                    if f.hardness:
                        draw_centered_string(self._graphics, (self._flags_position_layer_hardness, textY), self._flags_character, self.color_flag, self._default_bold_font)

                    if f.grain_type:
                        draw_centered_string(self._graphics, (self._flags_position_layer_grain_type, textY), self._flags_character, self.color_flag, self._default_bold_font)
                if flag_pos>0:
                    f = self._yellow_flags[flag_pos-1]
                    y = l.y2
                    if f.type() == YFValueType.LAYER_BOUNDARY:
                        if f.grain_size_difference:
                            draw_centered_string(self._graphics, (self._flags_position_boundary_grain_size_diff, y), self._flags_character, self.color_flag, self._default_bold_font)

                        if f.hardness_difference:
                            draw_centered_string(self._graphics, (self._flags_position_boundary_hardness_diff, y), self._flags_character, self.color_flag, self._default_bold_font)

                        if f.depth:
                            draw_centered_string(self._graphics, (self._flags_position_boundary_depth, y), self._flags_character, self.color_flag, self._default_bold_font)
                    if f.type() == YFValueType.LAYER_BOUNDARY and f.total_score > 0:
                        draw_centered_string(self._graphics, (self._flags_position_total_score, y), str(f.total_score), self.color_flag_total_score, self._default_bold_font)
                flag_pos +=2

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

