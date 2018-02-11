from iacs_profile. iacs_caaml_types import IACSHardnessType, IACSGrainShapeType
from utils.auto_enumerate import AutoName
from enum import auto
from collections import namedtuple, Set

_SUSPECTED_GRAIN_TYPES = [IACSGrainShapeType.FC, IACSGrainShapeType.FC_SO, IACSGrainShapeType.FC_SF,
                          IACSGrainShapeType.FC_XR, IACSGrainShapeType.DH, IACSGrainShapeType.DH_CP,
                          IACSGrainShapeType.DH_PR, IACSGrainShapeType.DH_CH, IACSGrainShapeType.DH_LA,
                          IACSGrainShapeType.DH_XR, IACSGrainShapeType.SH, IACSGrainShapeType.SH_SU,
                          IACSGrainShapeType.SH_CV, IACSGrainShapeType.SH_XR]


class YellowFlagsType(AutoName):
    GRAIN_SIZE = auto()
    HARDNESS = auto()
    GRAIN_TYPE = auto()
    GRAIN_SIZE_DIFF = auto()
    HARDNESS_DIFF = auto()
    DEPTH = auto()


class YFValueType(AutoName):
    LAYER = auto()
    LAYER_BOUNDARY = auto()


_YELLOW_FLAGS_FIELDS = ['presentation_depth', 'flags']


class LayerFlags(namedtuple('LayerFlags', _YELLOW_FLAGS_FIELDS)):

    def score(self):
        return len(self.flags)

    @staticmethod
    def layer_type():
        return YFValueType.LAYER


class LayerBoundaryFlags(namedtuple('LayerBoundaryFlags', _YELLOW_FLAGS_FIELDS + ['total_score'])):

    def score(self):
        return len(self.flags)

    @staticmethod
    def layer_type():
        return YFValueType.LAYER_BOUNDARY


def calculate_flags(profile):
    layer_flags = []
    previous_layer = None
    for l in profile.results.measurements.strat_profile:
        if previous_layer is not None:
            flags = set()
            if previous_layer.grain_size.avg.double_value != 0.0 and l.grain_size.avg.double_value != 0.0 and abs(previous_layer.grain_size.avg.double_value - l.grain_size.avg.double_value) > 0.5:
                flags.add(YellowFlagsType.GRAIN_SIZE_DIFF)
            if abs(previous_layer.hardness.cardinal_value.yf_value - l.hardness.cardinal_value.yf_value) > 1:
                flags.add(YellowFlagsType.HARDNESS_DIFF)
            if 20 <= l.depth_top <= 85:
                flags.add(YellowFlagsType.DEPTH)
            layer_flags.append(LayerBoundaryFlags(l.depth_top, flags, 0))
        flags = set()
        if l.grain_size.avg.double_value and l.grain_size.avg.double_value > 1:
            flags.add(YellowFlagsType.GRAIN_SIZE)
        if l.hardness.cardinal_value.yf_value < IACSHardnessType.F1.yf_value:
            flags.add(YellowFlagsType.HARDNESS)
        if l.grain_form_primary in _SUSPECTED_GRAIN_TYPES or l.grain_form_secondary in _SUSPECTED_GRAIN_TYPES:
            flags.add(YellowFlagsType.GRAIN_TYPE)
        layer_flags.append(LayerFlags(l.depth_top + (l.thickness) / 2, flags))
        previous_layer = l

    final_flags = []
    if len(layer_flags) > 2:
        previous_layer_flags = None
        previous_boundary_flags = None
        for f in layer_flags:
            if f.layer_type() == YFValueType.LAYER:
                if previous_layer_flags is not None and previous_boundary_flags is not None:
                    new_score = max(previous_layer_flags.score(), f.score())
                    previous_score = previous_boundary_flags.score()
                    final_flags.append(LayerBoundaryFlags(previous_boundary_flags.presentation_depth, previous_boundary_flags.flags, previous_score + new_score))
                    previous_boundary_flags = None
                previous_layer_flags = f
                final_flags.append(f)
            else:
                if f.layer_type() == YFValueType.LAYER_BOUNDARY:
                    previous_boundary_flags = f
    return final_flags
