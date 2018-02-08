from iacs_profile. iacs_caaml_types import IACSHardnessType, IACSGrainShapeType
from utils.auto_enumerate import AutoName
from enum import auto

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


class LayerFlags:
    presentation_depth = 0
    av_grain_size = False
    hardness = False
    grain_type = False

    def __init__(self, presentation_depth, av_grain_size, hardness, grain_type):
        self.presentation_depth = presentation_depth
        self.av_grain_size = av_grain_size
        self.hardness = hardness
        self.grain_type = grain_type

    def score(self):
        return self.av_grain_size + self.hardness + self.grain_type

    def type(self):
        return YFValueType.LAYER


class LayerBoundaryFlags:
    presentation_depth = 0
    grain_size_difference = False
    hardness_difference = False
    depth = False

    def __init__(self, presentation_depth, grain_size_difference, hardness_difference, _depth):
        self.presentation_depth = presentation_depth
        self.grain_size_difference = grain_size_difference
        self.hardness_difference = hardness_difference
        self.depth = _depth
        self.total_score = 0

    def score(self):
        return self.grain_size_difference + self.hardness_difference + self.depth

    def type(self):
        return YFValueType.LAYER_BOUNDARY


def calculate_flags(profile):
    flags = []
    previous_layer = None
    for l in profile.results.measurements.strat_profile:
        if previous_layer is not None:
            grain_size_difference = abs(previous_layer.grain_size.avg.double_value - l.grain_size.avg.double_value) > 0.5 if previous_layer.grain_size.avg.double_value != 0.0 and l.grain_size.avg.double_value != 0.0 else False
            hardness_difference = abs(previous_layer.hardness.cardinal_value.yf_value - l.hardness.cardinal_value.yf_value) > 1
            depth = 20 <= l.depth_top <= 85
            flags.append(LayerBoundaryFlags(l.depth_top, grain_size_difference, hardness_difference, depth))

        av_grain_size = l.grain_size.avg.double_value > 1 if l.grain_size.avg.double_value is not None else False
        hardness = l.hardness.cardinal_value.yf_value < IACSHardnessType.F1.yf_value
        grain_type = l.grain_form_primary in _SUSPECTED_GRAIN_TYPES or l.grain_form_secondary in _SUSPECTED_GRAIN_TYPES
        flags.append(LayerFlags(l.depth_top+(l.thickness)/2,av_grain_size, hardness, grain_type))
        previous_layer = l

    if len(flags) > 2:
        previous_layer_flags = None
        previous_boundary_flags = None
        for f in flags:
            if f.type() == YFValueType.LAYER:
                if previous_layer_flags is not None and previous_boundary_flags is not None:
                    new_score = max(previous_layer_flags.score(), f.score())
                    previous_score = previous_boundary_flags.score()
                    previous_boundary_flags.total_score =  previous_score + new_score
                    previous_boundary_flags = None
                previous_layer_flags = f
            else:
                if f.type() == YFValueType.LAYER_BOUNDARY:
                    previous_boundary_flags = f
    return flags