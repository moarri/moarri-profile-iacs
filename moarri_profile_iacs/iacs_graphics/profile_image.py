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

import os
import math

from PIL import Image, ImageColor, ImageDraw, ImageFont

from moarri_profile_iacs.iacs_graphics.tools import draw_centered_string
from moarri_profile_iacs.iacs_graphics.descritpion_columns import DescriptionColumnType, ColumnQualifier, DrawnColumn, \
    DrawnColumns, DrawnYellowFlagsColumn, YellowFlagsColumns, DEFAULT_COLUMN_SETTINGS, DEFAULT_YELLOW_FLAGS_NAMES
from moarri_profile_iacs.iacs_graphics.enum_font_code import *
from moarri_profile_iacs.iacs_profile.iacs_caaml_types import IACSHardnessType
from moarri_profile_iacs.profile_analysis.yellow_flags import calculate_flags, YFValueType

_SNOW_FONT_FILE_NAME = "SnowSymbolsIACS.ttf"
_DEFAULT_FONT_NAME = "arial.ttf"
_DEFAULT_BOLD_FONT_NAME = "arialbd.ttf"


class LayerDesc:

    def __init__(self, y1, y2, thickness, layer):
        self.y1 = y1
        self.y2 = y2
        self.thickness = thickness
        self.layer = layer


DEFAULT_BORDER_SETTINGS = {
    'width': 2,
    'color': ImageColor.colormap['black']
}


class ProfileGraphicsImage:

    _snow_profile = None
    _graphics = None

    _snow_font = None
    _default_font = None
    _default_bold_font = None
    _snow_font_size = 12

    _main_left_position = 0
    _main_right_position = 0
    _main_drawing_left_position = 0
    _main_drawing_right_position = 0

    _top_temp_position = 0

    _flags_character = "◄"

    temperatureUnitLabel = "-T[°C]"
    forceUnitLabel = "R[N]"

    font_size = 10
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
    opacityHandHardness = 128
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

    def __init__(self, snow_profile, width, height, page_width=0, page_height=0, top_x=0, top_y=0):
        self._snow_profile = snow_profile
        self._width = width
        self._height = height
        self._page_width = page_width if page_width > 0 else width
        self._page_height = page_height if page_height > 0 else height
        self._top_x = top_x
        self._top_y = top_y
        self._yellow_flags = calculate_flags(snow_profile)
        self._column_settings = DEFAULT_COLUMN_SETTINGS.copy()
        self._border_settings = DEFAULT_BORDER_SETTINGS.copy()
        self._yellow_flags_names = DEFAULT_YELLOW_FLAGS_NAMES.copy()
        self._drawn_columns = DrawnColumns()

    def _init_fonts(self):
        self._snow_font_size = int(0.8*self.minimalLayerThickness)
        snow_font_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', _SNOW_FONT_FILE_NAME))
        self._snow_font = ImageFont.truetype(snow_font_path, size=self._snow_font_size)
        self._default_font = ImageFont.truetype(_DEFAULT_FONT_NAME, size=self.font_size)
        self._default_bold_font = ImageFont.truetype(_DEFAULT_BOLD_FONT_NAME, size=self.font_size)

    def _init_image(self):
        self.image = Image.new('RGB', (self._page_width, self._page_height), self.colorBackground)
        self._graphics = ImageDraw.Draw(self.image)

    def _draw_border(self):
        border_color = self._border_settings['color']
        border_width = self._border_settings['width']
        half_of_border = border_width / 2
        left_top = (self._top_x + half_of_border, self._top_y + half_of_border)
        right_top = (self._top_x + self._width - border_width, self._top_y + half_of_border)
        right_bottom = (self._top_x + self._width - border_width, self._top_y + self._height - half_of_border)
        left_bottom = (self._top_x + half_of_border, self._top_y + self._height - half_of_border)
        self._graphics.line([left_top, right_top], fill=border_color, width=border_width)
        self._graphics.line([right_top, right_bottom], fill=border_color, width=border_width)
        self._graphics.line([right_bottom, left_bottom], fill=border_color, width=border_width)
        self._graphics.line([left_bottom, left_top], fill=border_color, width=border_width)

    def _calculate_temp_hardness_separator_position(self):
        return

    def _prepare_main_drawing_area_values(self):
        border_width = self._border_settings['width']
        self._main_left_position = self._top_x + border_width
        self._main_right_position = self._top_x + self._width - border_width - 1
        self.main_top_position = self._top_y + border_width
        self.temp_hardness_separator_position = self.main_top_position + self.temp_scale_height
        self.temp_text_vertical_position = self._main_left_position + int(
            (self.temp_scale_height - (self.tempHardnessSeparatorWidth / 2)) / 2)
        self.temp_unit_margin = self._graphics.textsize(self.temperatureUnitLabel)[0] + 3
        self.bottomInnerPosition = self._top_y + self._height - border_width - 1
        self.bottomHarndesScalePosition = self.main_top_position + self.temp_scale_height + self.hardnessScaleHeight
        self.hardnessTopPosition = self.bottomHarndesScalePosition + self.tempHardnessSeparatorWidth
        self.scaleVertical = (self.bottomInnerPosition - self.hardnessTopPosition) / (
                    self.maxSnowHeight - self.boottomOfGraph)
        self.hardnessTextVerticalPosition = self.main_top_position + self.temp_scale_height + int(
            self.tempHardnessSeparatorWidth / 2) + int((self.hardnessScaleHeight - self.tempHardnessSeparatorWidth) / 2)
        self._top_temp_position = self.temp_hardness_separator_position - (self.tempHardnessSeparatorWidth / 2)

    def _draw_inner_borders_scales_grids(self):
        border_width = self._border_settings['width']
        border_color = self._border_settings['color']
        self._graphics.line([self._main_left_position, self.bottomHarndesScalePosition, self._main_drawing_right_position,
                             self.bottomHarndesScalePosition], fill=border_color)
        self.forceUnitMargin = self._default_font.getsize(self.forceUnitLabel)[0] + 3
        draw_centered_string(self._graphics, (
            self._main_left_position + int(self.forceUnitMargin / 2), self.hardnessTextVerticalPosition),
                             self.forceUnitLabel,
                             self.text_color, self._default_font)
        self._graphics.line([self._main_left_position, self.temp_hardness_separator_position, self._main_right_position,
                             self.temp_hardness_separator_position], fill=border_color,
                            width=self.tempHardnessSeparatorWidth)
        draw_centered_string(self._graphics,
                             (self._main_left_position + (self.temp_unit_margin / 2), self.temp_text_vertical_position),
                             self.temperatureUnitLabel, self.text_color, self._default_font)

        self._draw_temperature_scales_grids()

        self._draw_hardness_scales_grids()

    def _draw_hardness_scales_grids(self):
        border_color = self._border_settings['color']
        self.scaleHorizontalHardness = (self._main_drawing_right_position - self._main_drawing_left_position) / 1200
        for h in range(200, 1000, 200):

            x = self._main_drawing_right_position - int(h * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x,
                                 self.temp_hardness_separator_position + self.mainMarkersLength],
                                fill=border_color)
            self._graphics.line([x, self.bottomHarndesScalePosition, x, self.bottomHarndesScalePosition - self.mainMarkersLength],
                                fill=border_color)
            if h <= 1000:
                draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), str(h), self.text_color,
                                     self._default_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)
        hardness_points = [IACSHardnessType.F, IACSHardnessType.F4, IACSHardnessType.F1, IACSHardnessType.P,
                           IACSHardnessType.K, IACSHardnessType.I]
        for htype in hardness_points:
            x = self._main_drawing_right_position - (htype.hardness * self.scaleHorizontalHardness)
            self._graphics.line([x, self.temp_hardness_separator_position, x,
                                 self.temp_hardness_separator_position + self.mainMarkersLength],
                                fill=border_color)
            self._graphics.line([x, self.bottomHarndesScalePosition, x, self.bottomHarndesScalePosition - self.mainMarkersLength],
                                fill=border_color)
            draw_centered_string(self._graphics, (x, self.hardnessTextVerticalPosition), htype.code, self.text_color,
                                 self._default_bold_font)
            self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition],
                                fill=self.color_hand_harness_grid)

    def _draw_temperature_scales_grids(self):
        border_color = self._border_settings['color']
        self.scaleHorizontalTemp = (self._main_drawing_right_position - self._main_left_position) / abs(self.minTemp)
        shift = 2 if abs(self.minTemp) > 24 else 1
        for t in range(0, abs(self.minTemp), shift):
            x = self._main_drawing_right_position - int(t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength],
                                fill=border_color)
            self._graphics.line([x, self._top_temp_position, x, self._top_temp_position - self.mainMarkersLength],
                                fill=border_color)
            label = str(t)
            label_width = self._default_font.getsize(label)[0]
            if (x + int(label_width / 2)) > (1 + self._main_left_position + self.temp_unit_margin):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color,
                                     self._default_font)
            if x > self._main_drawing_left_position and t > 0:
                self._graphics.line([x, self.hardnessTopPosition, x, self.bottomInnerPosition], fill=self.colorGrid)
        plus_temp_border = math.floor(
            (self._main_right_position - self._main_drawing_right_position) / self.scaleHorizontalTemp)
        for t in range(0, plus_temp_border, shift):
            x = self._main_drawing_right_position + (t * self.scaleHorizontalTemp)
            self._graphics.line([x, self.main_top_position, x, self.main_top_position + self.mainMarkersLength],
                                fill=border_color)
            self._graphics.line([x, self._top_temp_position, x, self._top_temp_position - self.mainMarkersLength],
                                fill=border_color)
            label = str(t)
            label_width = self._default_font.getsize(label)[0]
            if (x + (label_width / 2)) < (1 + self._main_right_position):
                draw_centered_string(self._graphics, (x, self.temp_text_vertical_position), label, self.text_color,
                                     self._default_font)

    def _draw_data_columns(self):
        border_color = self._border_settings['color']

        top_columns_position = self.temp_hardness_separator_position + int(self.tempHardnessSeparatorWidth / 2)
        last_column_border = self._main_right_position

        for dc in self._column_settings:
            if dc.present:
                if dc.column_type == DescriptionColumnType.SNOW_HEIGTH and dc.column_qualifier == ColumnQualifier.LEFT:
                    left_position = self._main_left_position
                    right_position = left_position + dc.width
                    last_column_border = left_position
                    text_position = right_position - int((dc.width - self.columnborder_width) / 2)
                    if len(dc.label) > 0:
                        draw_centered_string(self._graphics, (text_position, self.hardnessTextVerticalPosition),
                                             dc.label, self.text_color, self._default_font)
                    self._graphics.line(
                            [last_column_border, top_columns_position, last_column_border, self.bottomInnerPosition],
                            fill=border_color)
                    self._drawn_columns.add_column(DrawnColumn(dc.column_type, dc.column_qualifier, right_position,
                                                               left_position, dc.width, text_position));

                else:
                    right_position = last_column_border
                    left_position = right_position - dc.width
                    last_column_border = left_position
                    text_position = right_position - int((dc.width - self.columnborder_width) / 2)
                    if len(dc.label) > 0:
                        draw_centered_string(self._graphics, (text_position, self.hardnessTextVerticalPosition),
                                             dc.label, self.text_color, self._default_font)
                    self._graphics.line(
                            [last_column_border, top_columns_position, last_column_border, self.bottomInnerPosition],
                            fill=border_color)
                    if dc.column_type == DescriptionColumnType.YELLOW_FLAGS:
                        drawn_column = DrawnYellowFlagsColumn(dc.column_type, dc.column_qualifier, right_position,
                                                              left_position, dc.width, text_position,
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
                        drawn_column = DrawnColumn(dc.column_type, dc.column_qualifier, right_position,
                                                                 left_position, dc.width, text_position)
                    self._drawn_columns.add_column(drawn_column)
        leftSnowHeightColumn = self._drawn_columns.find_column(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.LEFT)
        self._main_drawing_left_position = leftSnowHeightColumn.right_border if leftSnowHeightColumn is not None else self._main_left_position
        self._main_drawing_right_position = self._drawn_columns.find_column(DescriptionColumnType.SNOW_HEIGTH,
                                                                            ColumnQualifier.MIDDLE).left_border
        for dc in self._drawn_columns.find_columns(DescriptionColumnType.SNOW_HEIGTH):
            self._draw_snow_heights(dc.left_border, dc.right_border,
                                    skip_last=(dc.column_qualifier == ColumnQualifier.LEFT))

    def _draw_snow_heights(self, left_position, rigth_position, skip_last=False):
        border_color = self._border_settings['color']

        center_depth_position = left_position + int((rigth_position - left_position - self.columnborder_width) / 2)
        for sh in range(self.boottomOfGraph, self.maxSnowHeight + 10, 10):
            y = self.bottomInnerPosition - ((sh - self.boottomOfGraph) * self.scaleVertical)
            self._graphics.line([left_position, y, left_position + self.mainMarkersLength, y],
                                fill=border_color)
            self._graphics.line(
                [rigth_position, y, rigth_position - self.mainMarkersLength, y],
                fill=border_color)
            if sh > self.boottomOfGraph:
                write_label = True if not skip_last else sh < self.maxSnowHeight
                if write_label:
                    draw_centered_string(self._graphics, (center_depth_position, y), str(sh), self.text_color,
                                         self._default_font)
                for i in range(2, 10, 2):
                    y1 = self.bottomInnerPosition - ((sh - i - self.boottomOfGraph) * self.scaleVertical)
                    self._graphics.line(
                        [left_position, y1, left_position + self.secondaryMarkersLength, y1],
                        fill=border_color)
                    self._graphics.line([rigth_position, y1,
                                         rigth_position - self.secondaryMarkersLength, y1],
                                        fill=border_color)

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
        right_line_x = self._main_drawing_right_position-1
        for l in layers:
            if first_layer:
                y = self.bottomInnerPosition - int((top_height - l.depth_top - self.boottomOfGraph) * self.scaleVertical)
                start = (right_line_x, y,)
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
                    last = (self._main_drawing_right_position - int(l.hardness.cardinal_value.hardness * self.scaleHorizontalHardness), y,)
                    layers_hardness.append(last)
            last_layer = l
        if last_layer is not None:
            y = self.bottomInnerPosition - int(
                (top_height - (last_layer.depth_top + last_layer.thickness) - self.boottomOfGraph) * self.scaleVertical)
            p1 = (last[0], y,)
            layers_hardness.append(p1)
            last = (right_line_x, y,)
            layers_hardness.append(last)
            # layersHardness.append(start)
            fill_color = ImageColor.getrgb(self.colorHandHardness)
            fill_color = (fill_color[0], fill_color[1], fill_color[2], self.opacityHandHardness)
            self._graphics.polygon(layers_hardness, fill=fill_color, outline=self.colorHandHardness)

            if last_layer.depth_top + last_layer.thickness > self.boottomOfGraph:
                y = last[1] + (self.handHardnessLineWidth / 2)
                # lineStroke = new BasicStroke(1)
                self._graphics.rectangle(
                    [self._main_drawing_left_position + 1, y, right_line_x, self.bottomInnerPosition],
                    fill=self.colorPitBaseSnow)

    def _create_layer_desc(self, l):
        th = int(l.thickness * self.scaleVertical)
        th = th if th >= self.minimalLayerThickness else self.minimalLayerThickness
        return LayerDesc(0, 0, th, l)

    def _draw_layers_desc(self, adjust_2_now_top=True):
        border_color = self._border_settings['color']
        if self._snow_profile is None:
            return
        layers = self._snow_profile.results.measurements.strat_profile
        top_height = self._snow_profile.results.measurements.hs.snow_height
        descs = [self._create_layer_desc(l) for l in layers]
        descs.append(LayerDesc(0, 0, 0, None))
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
                necessary_reduction = descs[0].y1 - descs[0].y2
                if adjust_2_now_top:
                    necessary_reduction = necessary_reduction if necessary_reduction <= possible_reduction else possible_reduction
                else:
                    text_gap = 3 * self._default_font.getsize("S")[1]
                    max_desc_position = self.hardnessTopPosition + text_gap
                    act_position = self.bottomInnerPosition - desc_thickness
                    necessary_reduction = max_desc_position - act_position
                while necessary_reduction > 0:
                    total_reduction = 0
                    for d in descs[-2::-1]:
                        if d.thickness > self.minimalLayerThickness and necessary_reduction > 0:
                            d.thickness -= 1
                            total_reduction += 1
                            necessary_reduction -= 1
                        d.y2 += total_reduction

        flag_pos = 0
        for l in descs:
            right_distance_column = self._drawn_columns.find_column(DescriptionColumnType.DISTANCE, ColumnQualifier.RIGHT)
            left_distance_column = self._drawn_columns.find_column(DescriptionColumnType.DISTANCE, ColumnQualifier.LEFT)
            left_left_distance_position = left_distance_column.left_border
            right_left_distance_position = left_distance_column.right_border
            left_rigth_distance_position = right_distance_column.left_border if right_distance_column else self._main_right_position
            right_rigth_distance_position = right_distance_column.right_border if right_distance_column else self._main_right_position
            self._graphics.line(
                [(left_left_distance_position, l.y1), (right_left_distance_position, l.y2)],
                fill=border_color, width=1)
            col = self._drawn_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
            x = col.left_border if col and l.layer  and flag_pos > 0 else left_rigth_distance_position
            self._graphics.line([(right_left_distance_position, l.y2), (x, l.y2)], fill=border_color,
                                width=1)
            self._graphics.line(
                [(left_rigth_distance_position, l.y2), (right_rigth_distance_position, l.y1)],
                fill=border_color, width=1)

            col = self._drawn_columns.find_column(DescriptionColumnType.SNOW_HEIGTH, ColumnQualifier.LEFT)
            if col:
                x1 = col.right_border
                x2 = x1 + self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=border_color, width=1)

            col = self._drawn_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
            if col:
                x1 = col.right_border
                x2 = x1 - self.mainMarkersLength
                self._graphics.line([(x1, l.y2), (x2, l.y2)], fill=border_color, width=1)
                x1 = col.left_border
                x2 = col.borders[2]
                self._graphics.line([(x1, l.y2), (x2, l.y2)], fill=border_color, width=1)
            col = self._drawn_columns.find_single_column(DescriptionColumnType.TESTS)
            if col:
                x1 = col.left_border
                x2 = x1 + self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=border_color, width=1)
                x1 = col.right_border
                x2 = x1 - self.mainMarkersLength
                self._graphics.line([(x1, l.y1), (x2, l.y1)], fill=border_color, width=1)

            text_y = l.y2 + int(l.thickness / 2)
            if l.layer is not None:
                col = self._drawn_columns.find_single_column(DescriptionColumnType.GRAIN_SIZE)
                if col:
                    avg = l.layer.grain_size.avg.double_value
                    avg_max = l.layer.grain_size.avg_max.double_value
                    text_avg = str(avg) if avg is not None and avg > 0.0 else ""
                    text_avg_max = str(avg_max) if avg_max is not None and avg_max > 0.0 else ""
                    txt = text_avg + " - " + text_avg_max
                    draw_centered_string(self._graphics, (col.text_position, text_y), txt,
                                         self.text_color, self._default_font)
                col = self._drawn_columns.find_single_column(DescriptionColumnType.GRAIN_SHAPE)
                if col and l.layer.grain_form_primary:
                    txt = IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_primary]
                    if l.layer.grain_form_secondary is not None and l.layer.grain_form_secondary != l.layer.grain_form_primary:
                        txt += IACS_GRAIN_SHAPE_TYPE_DICT[l.layer.grain_form_secondary]
                    draw_centered_string(self._graphics, (col.text_position, text_y), txt, self.text_color,
                                         self._snow_font)

                col = self._drawn_columns.find_single_column(DescriptionColumnType.HARDNESS)
                if col and l.layer.hardness.cardinal_value:
                    txt = IACS_HARDNESS_TYPE_DICT[l.layer.hardness.cardinal_value]
                    draw_centered_string(self._graphics, (col.text_position, text_y), txt, self.text_color,
                                         self._snow_font)
                col = self._drawn_columns.find_single_column(DescriptionColumnType.LWC)
                if col and l.layer.lwc.cardinal_value:
                    txt = IACS_LIQUID_WATER_CONTENT_TYPE_DICT[l.layer.lwc.cardinal_value]
                    draw_centered_string(self._graphics, (col.text_position, text_y), txt, self.text_color,
                                         self._snow_font)
                col = self._drawn_columns.find_single_column(DescriptionColumnType.YELLOW_FLAGS)
                if col:
                    f = self._yellow_flags[flag_pos]
                    for flag in f.flags:
                        yfc = YellowFlagsColumns.find_column(flag)
                        if yfc:
                            lbl = col.labels[yfc]
                            if lbl:
                                draw_centered_string(self._graphics, (lbl[0], text_y),
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
