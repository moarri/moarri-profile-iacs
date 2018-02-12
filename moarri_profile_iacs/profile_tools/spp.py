import operator

from moarri_profile_iacs.iacs_profile.iacs_caaml_types import *
from moarri_profile_iacs.iacs_profile.iacs_caaml_profile import *
class Section:
    name = ""
    start = 0
    end = 0

    def __init__(self, name, start):
        self.name = name
        self.start = start


def _check_section(l):
    if len(l) == 0:
        return False
    return l[0] == ":"


def _extract_section_name(l):
    subline = l[1:]
    pos = subline.find(":")
    return subline[0:pos] if pos > 0 else ""


def import_spp(filename):
    lines = []
    with open(filename, 'r') as ifile:
        lines = ifile.readlines()
    actual_section = None
    sections = {}
    for i, l in enumerate(lines):
        line = l.strip()
        if _check_section(line):
            section_name = _extract_section_name(line)
            if actual_section is not None:
                actual_section.end = i-1
                sections[actual_section.name] = actual_section
            actual_section = Section(section_name, i+1)
    if actual_section is not None:
        actual_section.end = len(lines)-1
        sections[actual_section.name] = actual_section

    profile_desc_section = sections['KOPF']
    measurements = _parse_profile_desc(lines[profile_desc_section.start:profile_desc_section.end+1])
    temp_profile_section = sections['TEMP-SCHICHTEN']
    measurements['temp_profile'] = _parse_temp_profile(lines[temp_profile_section.start:temp_profile_section.end+1])
    hand_snow_profile_section = sections['SCHNEE-SCHICHTEN']
    snow_height, hand_snow_profile = _parse_hand_snow_profile(lines[hand_snow_profile_section.start:hand_snow_profile_section.end+1])
    measurements['profile_depth'] = snow_height
    measurements['hs'] = SnowHeightComponents.create_default(snow_height)
    measurements['strat_profile'] = hand_snow_profile
    return SnowProfile("1", SnowProfileResults(SnowProfileMeasurements.create_default(**measurements)))


_LWC_DICT = {
    (1, 1): IACSLiquidWaterContentType.D,
    (1, 2): IACSLiquidWaterContentType.DM,
    (2, 2): IACSLiquidWaterContentType.M,
    (2, 3): IACSLiquidWaterContentType.MW,
    (3, 3): IACSLiquidWaterContentType.W,
    (3, 4): IACSLiquidWaterContentType.WV,
    (4, 4): IACSLiquidWaterContentType.V,
    (4, 5): IACSLiquidWaterContentType.VS,
    (5, 5): IACSLiquidWaterContentType.S
}

_GRAIN_FORM_DICT = {
    0: IACSGrainShapeType.PP_GP,
    1: IACSGrainShapeType.PP,
    2: IACSGrainShapeType.DF,
    3: IACSGrainShapeType.RG,
    4: IACSGrainShapeType.FC,
    5: IACSGrainShapeType.DH,
    6: IACSGrainShapeType.SH,
    7: IACSGrainShapeType.MF,
    8: IACSGrainShapeType.IF,
    9: IACSGrainShapeType.FC_XR
}

_HAND_HARDNESS_DICT = {
    (1, 1): IACSHardnessType.F,
    (1, 2): IACSHardnessType.FF4,
    (2, 2): IACSHardnessType.F4,
    (2, 3): IACSHardnessType.F4F1,
    (3, 3): IACSHardnessType.F1,
    (3, 4): IACSHardnessType.F1P,
    (4, 4): IACSHardnessType.P,
    (4, 5): IACSHardnessType.PK,
    (5, 5): IACSHardnessType.K,
    (5, 6): IACSHardnessType.KI,
    (6, 6): IACSHardnessType.I
}


def _translate_lwc(w1, w2):
    return _LWC_DICT[(w1, w2)] if (w1, w2) in _LWC_DICT else None


def _translate_grain_form(f1, f2, f3):
    return (IACSGrainShapeType.MF_CR, IACSGrainShapeType.MF_CR) if f3 == 2 else (_GRAIN_FORM_DICT[f1], _GRAIN_FORM_DICT[f2])


def _translate_hand_hardness(k1, k2):
    hrd = _HAND_HARDNESS_DICT[(k1, k2)] if (k1, k2) in _HAND_HARDNESS_DICT else None
    return hrd


class TempObs:
    def __init__(self, depth_top, grain_form_primary, grain_form_secondary, grain_size, hardness, lwc):
        self.depth_top = depth_top
        self.thickness = 0.0
        self.grain_form_primary = grain_form_primary
        self.grain_form_secondary = grain_form_secondary
        self.grain_size = grain_size
        self.hardness = hardness
        self.lwc = lwc

    def to_caaml_layer(self):
        return StratProfileLayer.create_default(self.depth_top, self.thickness, None, self.grain_form_primary, self.grain_form_secondary, self.grain_size, self.hardness, self.lwc)


def _parse_hand_snow_profile(lines):
    h = lines[::10]
    d1 = lines[1::10]
    d2 = lines[2::10]
    w1 = lines[3::10]
    w2 = lines[4::10]
    f1 = lines[5::10]
    f2 = lines[6::10]
    f3 = lines[7::10]
    k1 = lines[8::10]
    k2 = lines[9::10]
    obs = [x for x in zip(h, d1, d2, w1, w2, f1, f2, f3, k1, k2)]
    snow_height = max([float(x[0])/10.0 for x in obs])
    observations = []
    for o in obs:
        depth_top = snow_height-(float(o[0])/10.0)
        grain_size = GrainSize.create_default(float(o[1])/100.0, float(o[2])/100.0)
        lwc = Lwc.create_cardinal(_translate_lwc(int(o[3]), int(o[4])))
        grain_forms = _translate_grain_form(int(o[5]), int(o[6]), int(o[7]))
        grain_form_primary = grain_forms[0]
        grain_form_secondary = grain_forms[1]
        hardness = Hardness.create_cardinal(_translate_hand_hardness(int(o[8]), int(o[9])))
        observations.append(TempObs(depth_top, grain_form_primary, grain_form_secondary, grain_size, hardness, lwc))
    observations.sort(key=operator.attrgetter('depth_top'), reverse=False)
    previous_layer = observations[0]
    for o in observations[1:]:
        previous_layer.thickness = o.depth_top - previous_layer.depth_top
        previous_layer = o
    observations[-1].thickness = snow_height - observations[-1].depth_top
    return snow_height, [x.to_caaml_layer() for x in observations]


def _parse_temp_profile(lines):
    th = lines[::2]
    tt = lines[1::2]
    obs = [x for x in zip(th, tt)]
    snow_height = max([float(x[0])/10.0 for x in obs])
    observations = []
    for o in obs:
        observations.append(TempProfileObs.create_default(snow_height-(float(o[0])/10.0), -float(o[1])/10.0))
    observations.sort(key=operator.attrgetter('depth'), reverse=False)
    return TempProfile.create_default(observations)


def _parse_profile_desc(lines):
    measurements = {}
    if len(lines) > 27:
        measurements['comment'] = lines[26]
    wind_dir = IACSAspectCardinalType.value_of(lines[3].strip('\n'))
    measurements['wind_dir'] = Aspect.create_default(wind_dir if wind_dir is not None else IACSAspectCardinalType.N_A)
    wind_speed_str = lines[11].strip('\n')
    if len(wind_speed_str) > 0:
        measurements['wind_spd'] = float(wind_speed_str)/10.0/3.6
    measurements['air_temp_pres'] = float(lines[15])/10

    area=lines[0][0:2]
    location=lines[0][2:]
    persons=lines[1]
    exposition= lines[6]
    slope_angle= lines[14]
    return measurements

