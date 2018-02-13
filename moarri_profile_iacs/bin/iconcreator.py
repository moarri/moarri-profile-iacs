# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

import os
import sys
from PIL import Image, ImageColor, ImageDraw, ImageFont

from moarri_profile_iacs.iacs_graphics.enum_font_code import *

_SNOW_FONT_FILE_NAME = "IACSSnow.ttf"


def _create_icon(size, text, snow_font, filename):
    print(filename)
    text_size = snow_font.getsize(text)
    width = round(1.11 * text_size[0])
    image = Image.new('RGB', (width, size), (255, 255, 255))
    graphics = ImageDraw.Draw(image)
    graphics.text((int(width/2 - text_size[0] / 2), int(size/2 - text_size[1] / 2)), text, fill=(0,0,0), font=snow_font)
    image.save(filename, 'PNG')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage program dest_dir")
        exit(0)
    base_dir = sys.argv[1]
    for size in [8, 12, 24, 32, 36, 48, 64, 72, 128]:
        final_path = os.path.join(base_dir, str(size))
        os.makedirs(final_path, exist_ok=True)
        font_size = int(0.9 * size)
        snow_font_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'iacs_graphics', '' 'fonts', _SNOW_FONT_FILE_NAME))
        snow_font = ImageFont.truetype(snow_font_path, size=font_size)
        for s in IACS_GRAIN_SHAPE_TYPE_DICT:
            _create_icon(size, IACS_GRAIN_SHAPE_TYPE_DICT[s], snow_font, os.path.join(final_path,s.code+".png"))
        for s in IACS_HARDNESS_TYPE_DICT:
            _create_icon(size, IACS_HARDNESS_TYPE_DICT[s], snow_font, os.path.join(final_path,s.code+".png"))
        for s in IACS_LIQUID_WATER_CONTENT_TYPE_DICT:
            _create_icon(size, IACS_LIQUID_WATER_CONTENT_TYPE_DICT[s], snow_font, os.path.join(final_path,s.code+".png"))
