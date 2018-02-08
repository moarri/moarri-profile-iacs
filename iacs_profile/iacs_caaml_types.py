# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

from iacs_profile.codeable_enum import CodeableEnum


class IACSAspectCardinalType(CodeableEnum):
    N = ("N")
    NE = ("NE")
    E = ("E")
    SE = ("SE")
    S = ("S")
    SW = ("SW")
    W = ("W")
    NW = ("NW")
    N_A = ("n/a")


class IACSDirectionType(CodeableEnum):
    TOP_DOWN = ("top down")
    BOTTOM_UP = ("bottom up")


class IACSGrainShapeType(CodeableEnum):
    PP = ('PP')
    PP_CO = ('PPco')
    PP_ND = ('PPnd')
    PP_PL = ('PPpl')
    PP_SD = ('PPsd')
    PP_IR = ('PPir')
    PP_GP = ('PPgp')
    PP_HL = ('PPhl')
    PP_IP = ('PPip')
    PP_RM = ('PPrm')
    MM = ('MM')
    MM_RP = ('MMrp')
    MM_CI = ('MMci')
    DF = ('DF')
    DF_DC = ('DFdc')
    DF_BK = ('DFbk')
    RG = ('RG')
    RG_SR = ('RGsr')
    RG_LG = ('RGlg')
    RG_WP = ('RGwp')
    RG_XF = ('RGxf')
    FC = ('FC')
    FC_SO = ('FCso')
    FC_SF = ('FCsf')
    FC_XR = ('FCxr')
    DH = ('DH')
    DH_CP = ('DHcp')
    DH_PR = ('DHpr')
    DH_CH = ('DHch')
    DH_LA = ('DHla')
    DH_XR = ('DHxr')
    SH = ('SH')
    SH_SU = ('SHsu')
    SH_CV = ('SHcv')
    SH_XR = ('SHxr')
    MF = ('MF')
    MF_CL = ('MFcl')
    MF_PC = ('MFpc')
    MF_SL = ('MFsl')
    MF_CR = ('MFcr')
    IF = ('IF')
    IF_IL = ('IFil')
    IF_IC = ('IFic')
    IF_BI = ('IFbi')
    IF_RC = ('IFrc')
    IF_SC = ('IFsc')

    def is_parent(self):
        if len(self.children()) > 0:
            return True
        return False

    def children(self):
        if len(self.code) > 2:
            return []
        return [x for x in list(IACSGrainShapeType) if x.code.startswith(self.code) and len(x.code)>2]


class IACSGrainSizeType(CodeableEnum):
    pass


class IACSHardnessType(CodeableEnum):
    F_MINUS = ('F-', 10, 0.75)
    F = ('F', 20, 1)
    F_PLUS = ('F+', 35, 1.25)
    FF4 = ('F-4F', 50, 1.5)
    F4_MINUS = ('4F-', 75, 1.75)
    F4 = ('4F', 100, 2)
    F4_PLUS = ('4F+', 137, 2.25)
    F4F1 = ('4F-1F', 175, 2.5)
    F1_MINUS = ('1F-', 210, 2.75)
    F1 = ('1F', 250, 3)
    F1_PLUS = ('1F+', 235, 3.25)
    F1P = ('1F-P', 390, 3.5)
    P_MINUS = ('P-', 445, 3.75)
    P = ('P', 500, 4)
    P_PLUS = ('P+', 605, 4.25)
    PK = ('P-K', 715, 4.5)
    K_MINUS = ('K-', 900, 4.75)
    K = ('K', 1000, 5)
    K_PLUS = ('K+', 1100, 5.25)
    KI = ('K-I', 1150, 5.5)
    I_MINUS = ('I-', 1175, 5.75)
    I = ('I', 1200, 6)

    def __init__(self, code, hardness, yf_value):
        self.code = code
        self.hardness = hardness
        self.yf_value = yf_value


class IACSLiquidWaterContentType(CodeableEnum):
    D = ('D')
    DM = ('D-M')
    M = ('M')
    MW = ('M-W')
    W = ('W')
    WV = ('W-V')
    V = ('V')
    VS = ('V-S')
    S = ('S')


class IACSNilReasonType(CodeableEnum):
    INAPPLICABLE = ('inapplicable')
    MISSING = ('missing')
    TEMPLATE = ('template')
    UNKNOWN = ('unknown')
    WITHHELD = ('withheld')


class IACSPrecipTIType(CodeableEnum):
    DZ_MINUS = ('-DZ')
    DZ = ('DZ')
    DZ_PLUS = ('+DZ')
    RA_MINUS = ('-RA')
    RA = ('RA')
    RA_PLUS = ('+RA')
    SN_MINUS = ('-SN')
    SN = ('SN')
    SN_PLUS = ('+SN')
    SG_MINUS = ('-SG')
    SG = ('SG')
    SG_PLUS = ('+SG')
    IC_MINUS = ('-IC')
    IC = ('IC')
    IC_PLUS = ('+IC')
    PE_MINUS = ('-PE')
    PE = ('PE')
    PE_PLUS = ('+PE')
    GR_MINUS = ('-GR')
    GR = ('GR')
    GR_PLUS = ('+GR')
    GS_MINUS = ('-GS')
    GS = ('GS')
    GS_PLUS = ('+GS')
    UP = ('UP')
    NIL = ('Nil')
    RASN = ('RASN')
    FZRA = ('FZRA')


class IACSSkyConditionType(CodeableEnum):
    CLR = ('CLR')
    FEW = ('FEW')
    SCI = ('SCT')
    BKN = ('BKN')
    OVC = ('OVC')
    X = ('X')


class IACSSurfaceRoughnessType(CodeableEnum):
    RSM = ('rsm')
    RWA = ('rwa')
    RCV = ('rcv')
    RCX = ('rcx')
    RRD = ('rrd')


class IACSUnitsAreaType(CodeableEnum):
    M2 = ('m2')


class IACSUnitsDensityType(CodeableEnum):
    KGM3 = ('kgm-3')


class IACSUnitsForceType(CodeableEnum):
    N = ('N')
    EMPTY = ('')


class IACSUnitsInclineType(CodeableEnum):
    DEG = ('deg')


class IACSUnitsLengthType(CodeableEnum):
    CM = ('cm')
    MM = ('mm')
    M = ('m')
    IN = ('in')
    FT = ('ft')


class IACSUnitsLwcType(CodeableEnum):
    PRCVOL = ('% per Vol')
    EMPTY = ('')


class IACSUnitsPressureType(CodeableEnum):
    NM2 = ('Nm-2')
    PA = ('Pa')


class IACSUnitsSpecSurfAreaType(CodeableEnum):
    M2KG1 = ('m2kg-1')


class IACSUnitsTempType(CodeableEnum):
    DEGC = ('degC')


class IACSUnitsUnitType(CodeableEnum):
    ONE = ('1')


class IACSUnitsWeightType(CodeableEnum):
    KG = ('kg')


class IACSUnitsWindSpdType(CodeableEnum):
    MS1 = ('ms-1')
    EMPTY = ('')


class IACSWindSpdType(CodeableEnum):
    C = ('C')
    L = ('L')
    M = ('M')
    S = ('S')
    X = ('X')


def IACSComprTestScoreCatType(CodeableEnum):
    CTV = ("CTV")
    CTE = ("CTE")
    CTM = ("CTM")
    CTH = ("CTH")


class IACSComprTestScoreNumType(CodeableEnum):
    CT_0 = ('0')
    CT_01 = ('1')
    CT_02 = ('2')
    CT_03 = ('3')
    CT_04 = ('4')
    CT_05 = ('5')
    CT_06 = ('6')
    CT_07 = ('7')
    CT_08 = ('8')
    CT_09 = ('9')
    CT_10 = ('10')
    CT_11 = ('11')
    CT_12 = ('12')
    CT_13 = ('13')
    CT_14 = ('14')
    CT_15 = ('15')
    CT_16 = ('16')
    CT_17 = ('17')
    CT_18 = ('18')
    CT_19 = ('19')
    CT_20 = ('20')
    CT_21 = ('21')
    CT_22 = ('22')
    CT_23 = ('23')
    CT_24 = ('24')
    CT_25 = ('25')
    CT_26 = ('26')
    CT_27 = ('27')
    CT_28 = ('28')
    CT_29 = ('29')
    CT_30 = ('30')

    def int_val(self):
        return int(self.code)

# TODO implement categorisation of CT codes
    def to_cat_type(self):
        v = self.int_val()
        return None

def IACSComprTestScoreCatType(CodeableEnum):
    CTV = ("CTV")
    CTE = ("CTE")
    CTM = ("CTM")
    CTH = ("CTH")