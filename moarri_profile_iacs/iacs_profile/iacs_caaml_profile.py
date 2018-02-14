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

from collections import namedtuple
from moarri_profile_iacs.iacs_profile.iacs_caaml_types import *
from moarri_profile_iacs.iacs_profile.iacs_caaml_meta import *


class SnowHeightComponents(namedtuple('SnowHeightComponents', ('components_type', 'snow_height', 'snow_height_uom',
                                                               'swe', 'swe_uom'))):

    @classmethod
    def create_default(cls, snow_height):
        return SnowHeightComponents(SnowHeightComponentsType.SNOW_HEIGHT, snow_height, IACSUnitsLengthType.CM, None,
                                    None)

    @classmethod
    def create_snow_height(cls, snow_height, snow_height_uom):
        return SnowHeightComponents(SnowHeightComponentsType.SNOW_HEIGHT, snow_height, snow_height_uom, None,
                                    None)

    @classmethod
    def create_swe(cls, swe, swe_uom):
        return SnowHeightComponents(SnowHeightComponentsType.WATER_EQUIWALENT, None, None, swe, swe_uom)

    @classmethod
    def create_both(cls, snow_height, snow_height_uom, swe, swe_uom):
        return SnowHeightComponents(SnowHeightComponentsType.BOTH, snow_height, snow_height_uom, swe, swe_uom)


class LayerPointObsRoot(namedtuple('LayerPointObsRoot', '')):
    pass


class PointObsInProfileBase(namedtuple('PointObsInProfileBase', LayerPointObsRoot._fields + ('depth', 'depth_uom'))):

    @classmethod
    def create_default(cls, depth):
        return PointObsInProfileBase(depth, IACSUnitsLengthType.CM)


class LayerInProfileBase(namedtuple('LayerInProfileBase', LayerPointObsRoot._fields + ('depth_top', 'depth_top_uom',
                                                                                       'thickness', 'thickness_uom'))):

    @classmethod
    def create_default(cls, depth_top, thickness):
        return LayerInProfileBase(depth_top, IACSUnitsLengthType.CM, thickness, IACSUnitsLengthType.CM)


class StratigraphicLayerBase(
    namedtuple('StratigraphicLayerBase', LayerInProfileBase._fields + ('validFormationTime',))):

    @classmethod
    def create_default(cls, depth_top, thickness, validFormationTime):
        return StratigraphicLayerBase(depth_top, IACSUnitsLengthType.CM, thickness, IACSUnitsLengthType.CM,
                                      validFormationTime)


class TempProfile(namedtuple('TempProfile', ('temp_profile', 'temp_profile_uom_depth', 'temp_profile_uom_temp'))):

    @classmethod
    def create_default(cls, temp_profile):
        return TempProfile(temp_profile, IACSUnitsLengthType.CM, IACSUnitsTempType.DEGC)


class TempProfileObs(namedtuple('TempProfileObs', PointObsInProfileBase._fields + ('snow_temp',))):

    @classmethod
    def create_default(cls, depth, snow_temp):
        return TempProfileObs(depth, IACSUnitsLengthType.CM, snow_temp)


class Aspect(namedtuple('Aspect', ('aspect_type', 'aspect_position'))):

    @classmethod
    def create_default(cls, aspect_position):
        return Aspect(CompositeValueType.CARDINAL, aspect_position)


class GrainSizeComponent(namedtuple('GrainSizeComponent', ['grain_size_type', 'cardinal_value', 'double_value'])):

    @classmethod
    def create_cardinal(cls, cardinal_value):
        return GrainSizeComponent(CompositeValueType.CARDINAL, cardinal_value, None)

    @classmethod
    def create_numeric(cls, double_value):
        return GrainSizeComponent(CompositeValueType.NUMERIC, None, double_value)


class GrainSize(namedtuple('GrainSize', ['uom', 'avg', 'avg_max'])):

    @classmethod
    def create(cls, uom, avg, avg_max):
        return GrainSize(uom, GrainSizeComponent.create_numeric(avg), GrainSizeComponent.create_numeric(avg_max))

    @classmethod
    def create_default(cls, avg, avg_max):
        return GrainSize(IACSUnitsLengthType.MM, GrainSizeComponent.create_numeric(avg),
                         GrainSizeComponent.create_numeric(avg_max))


class Hardness(namedtuple('Hardness', ['hardness_type', 'uom', 'double_value', 'cardinal_value'])):

    @classmethod
    def create_cardinal(cls, cardinal_value):
        return Hardness(CompositeValueType.CARDINAL, IACSUnitsForceType.EMPTY, None, cardinal_value)

    @classmethod
    def create_numeric(cls, double_value):
        return Hardness(CompositeValueType.NUMERIC, IACSUnitsForceType.N, double_value, None)


class Lwc(namedtuple('Lwc', ['lwc_type', 'uom', 'double_value', 'cardinal_value'])):

    @classmethod
    def create_cardinal(cls, cardinal_value):
        return Lwc(CompositeValueType.CARDINAL, IACSUnitsLwcType.EMPTY, None, cardinal_value)

    @classmethod
    def create_numeric(cls, double_value):
        return Lwc(CompositeValueType.NUMERIC, IACSUnitsLwcType.PRCVOL, double_value, None)


class StratProfileLayer(namedtuple('StratProfileLayer', StratigraphicLayerBase._fields + ('grain_form_primary',
                                                                                          'grain_form_secondary',
                                                                                          'grain_size', 'hardness',
                                                                                          'lwc'))):

    @classmethod
    def create_default(cls, depth_top, thickness, valid_formation_time, grain_form_primary, grain_form_secondary,
                       grain_size, hardness, lwc):
        return StratProfileLayer(depth_top, IACSUnitsLengthType.CM, thickness, IACSUnitsLengthType.CM,
                                 valid_formation_time, grain_form_primary, grain_form_secondary, grain_size, hardness,
                                 lwc)


class CompressionTestFailedOn(namedtuple('CompressionTest', ('layer', 'results'))):
    pass


_MEASUREMENTS_FIELDS = ['direction', 'comment', 'profile_depth', 'profile_depth_uom', 'sky_cond', 'precip_ti',
                        'air_temp_pres', 'air_temp_pres_uom', 'wind_spd', 'wind_dir', 'wind_spd_uom', 'hs',
                        'hn24', 'hin', 'penetration_ram', 'penetration_ram_uom', 'penetration_foot',
                        'penetration_foot_uom', 'penetration_ski', 'penetration_ski_uom', 'strat_profile',
                        'temp_profile', 'stability_tests']


class SnowProfileMeasurements(namedtuple('SnowProfileMeasurements', _MEASUREMENTS_FIELDS)):

    @classmethod
    def create_default(cls, **kwargs):
        defaults = {
            'direction': IACSDirectionType.TOP_DOWN,
            'comment': None,
            'profile_depth': 0.0,
            'profile_depth_uom': IACSUnitsLengthType.CM,
            'sky_cond': None,
            'precip_ti': None,
            'air_temp_pres': 0.0,
            'air_temp_pres_uom': IACSUnitsTempType.DEGC,
            'wind_spd': 0.0,
            'wind_dir': None,
            'wind_spd_uom': IACSUnitsWindSpdType.MS1,
            'hs': None,
            'hn24': None,
            'hin': None,
            'penetration_ram': 0.0,
            'penetration_ram_uom': IACSUnitsLengthType.CM,
            'penetration_foot': 0.0,
            'penetration_foot_uom': IACSUnitsLengthType.CM,
            'penetration_ski': 0.0,
            'penetration_ski_uom': IACSUnitsLengthType.CM,
            'strat_profile': None,
            'temp_profile': None,
            'stability_tests': None
        }
        for a in kwargs.items():
            if a[0] in defaults:
                defaults[a[0]] = a[1]
        return SnowProfileMeasurements(**defaults)


class SnowProfileResults(namedtuple('SnowProfileResults', ('measurements',))):
    pass


class SnowProfile(namedtuple('SnowProfile', ('profile_id', 'results'))):
    pass
