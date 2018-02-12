# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

import os
from PIL import Image
from moarri_profile_iacs.iacs_profile.iacs_caaml_types import IACSGrainShapeType, IACSHardnessType, IACSLiquidWaterContentType

_ICON_PATH = "../resources/icons"
_ICON_SIZES = [8, 12, 24, 32, 36, 48, 64, 72, 128]


def _create_icon_path(code, size):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), _ICON_PATH, str(size), code+".png")
    return os.path.abspath(path)


class IconProvider:
    def __init__(self, size):
        smaller_ro_equal = [x for x in _ICON_SIZES if size >= x]
        icon_size = smaller_ro_equal[-1] if len(smaller_ro_equal)>0 else _ICON_SIZES[0]
        self._icons = {}
        for item in IACSGrainShapeType:
            self._icons[item.code] = Image.open(_create_icon_path(item.code, icon_size))
        for item in IACSHardnessType:
            self._icons[item.code] = Image.open(_create_icon_path(item.code, icon_size))
        for item in IACSLiquidWaterContentType:
            self._icons[item.code] = Image.open(_create_icon_path(item.code, icon_size))

    def find_image(self, code):
        return self._icons[code] if code in self._icons else None
