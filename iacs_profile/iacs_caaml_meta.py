# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

from utils.enumeratings import CodeableEnum
from enum import Enum

ATTR_UOM = "uom"
UOM_DEPTH = "uomDepth"
UOM_TEMP = "uomTemp"


class CompositeValueType(Enum):
    CARDINAL = 1
    NUMERIC = 2


class UnitSystem(Enum):
    METRIC = 1
    IMPERIAL = 2


class SnowHeightComponentsType(Enum):
    SNOW_HEIGHT = 1
    WATER_EQUIWALENT = 2
    BOTH = 3


class LayerMeta(CodeableEnum):
    MAIN_NODE = ('Layer')
    CHILD_DEPTH_TOP = ('depthTop')
    CHILD_THICKNESS = ('thickness')
    CHILD_GRAIN_FORM_PRIMARY = ('grainFormPrimary')
    CHILD_GRAIN_FORM_SECONDARY = ('grainFormSecondary')
    CHILD_GRAIN_SIZE = ('grainSize')
    CHILD_HARDNESS = ('hardness')
    CHILD_LWC = ('lwc')


class GrainSizeMeta(CodeableEnum):
    MAIN_NODE = ('Components')
    CHILD_AVG = ('avg')
    CHILD_AVG_MAX = ('avgMax')


class AspectMeta(CodeableEnum):
    MAIN_NODE = ('AspectPosition')
    CHILD_POSITION = ('position')


class SnowHeightComponentsMeta(CodeableEnum):
    MAIN_NODE = ('Components')
    CHILD_SNOW_HEIGHT = ('snowHeight')
    CHILD_SWE = ('swe')


class SnowProfileMeasurementsMeta(CodeableEnum):
    MAIN_NODE = ('SnowProfileMeasurements')
    ATTR_DIR = ('dir')
    CHILD_COMMENT = ('comment')
    CHILD_PROFILE_DEPTH = ('profileDepth')
    CHILD_PENETRATION_RAM = ('penetrationRam')
    CHILD_PENETRATION_FOOT = ('penetrationFoot')
    CHILD_PENETRATION_SKI = ('penetrationSki')
    CHILD_AIR_TEMP_PRES = ('airTempPres')
    CHILD_WIND_SPD = ('windSpd')
    CHILD_WIND_DIR = ('windDir')
    CHILD_HS = ('hS')
    CHILD_HN24 = ('hN24')
    CHILD_HIN = ('hIN')
    CHILD_SKY_COND = ('skyCond')
    CHILD_PRECIP_TI = ('precipTI')
    CHILD_STRAT_PROFILE = ('stratProfile')
    CHILD_TEMP_PROFILE = ('tempProfile')
    CHILD_STABILITY_TESTS = ('stbTests')


class CompressionTestMeta(CodeableEnum):
    MAIN_NODE = ('ComprTest')
    CHILD_FAILED_ON = ('failedOn')

class CompressionTestFailedOnMeta(CodeableEnum):
    MAIN_NODE = ('failedOn')
    CHILD_LAYER = ('Layer')
    CHILD_RESULTS = ('Results')



class TempProfileObsMeta(CodeableEnum):
    MAIN_NODE = ('Obs')
    CHILD_DEPTH = ('depth')
    CHILD_SNOW_TEMP = ('snowTemp')


class SnowProfileMeta(CodeableEnum):
    MAIN_NODE = ('SnowProfile')
    ATTR_GML_ID = ('gml:id')
    ATTR_XMLNS = ('xmlns')
    ATTR_XMLNS_VALUE = ('http://caaml.org/Schemas/V5.0/Profiles/SnowProfileIACS')
    ATTR_XMLNS_GML = ('xmlns:gml')
    ATTR_XMLNS_GML_VALUE = ('http://www.opengis.net/gml')
    ATTR_XMLNS_APP = ('xmlns:app')
    ATTR_XMLNS_APP_VALUE = ('http://www.snowprofileapplication.com')
    ATTR_XMLNS_XSI = ('xmlns:xsi')
    ATTR_XMLNS_XSI_VALUE = ('http://www.w3.org/2001/XMLSchema-instance')
    ATTR_XSI_SCHEMA_LOCATION = ('xsi:schemaLocation')
    ATTR_XSI_SCHEMA_LOCATION_VALUE = ('http://caaml.org/Schemas/V5.0/Profiles/SnowProfileIACS http://caaml.org/Schemas/V5.0/Profiles/SnowprofileIACS/CAAMLv5_SnowProfileIACS.xsd')
    CHILD_META_DATA_PROPERTY = ('metaDataProperty')
    CHILD_VALID_TIME = ('validTime')
    CHILD_SNOW_PROFILE_RESULTS_OF = ('snowProfileResultsOf')
    CHILD_LOC_REF = ('locRef')

