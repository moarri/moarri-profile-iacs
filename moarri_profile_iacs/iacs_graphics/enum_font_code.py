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

from moarri_profile_iacs.iacs_profile.iacs_caaml_types import IACSGrainShapeType, IACSHardnessType, IACSLiquidWaterContentType

IACS_GRAIN_SHAPE_TYPE_DICT = {
    IACSGrainShapeType.PP: "a",
    IACSGrainShapeType.PP_CO: "j",
    IACSGrainShapeType.PP_ND: "k",
    IACSGrainShapeType.PP_PL: "l",
    IACSGrainShapeType.PP_SD: "m",
    IACSGrainShapeType.PP_IR: "n",
    IACSGrainShapeType.PP_GP: "o",
    IACSGrainShapeType.PP_HL: "p",
    IACSGrainShapeType.PP_IP: "q",
    IACSGrainShapeType.PP_RM: "r",
    IACSGrainShapeType.MM: "b",
    IACSGrainShapeType.MM_RP: "s",
    IACSGrainShapeType.MM_CI: "t",
    IACSGrainShapeType.DF: "c",
    IACSGrainShapeType.DF_DC: "u",
    IACSGrainShapeType.DF_BK: "v",
    IACSGrainShapeType.RG: "d",
    IACSGrainShapeType.RG_SR: "w",
    IACSGrainShapeType.RG_LG: "x",
    IACSGrainShapeType.RG_WP: "y",
    IACSGrainShapeType.RG_XF: "z",
    IACSGrainShapeType.FC: "e",
    IACSGrainShapeType.FC_SO: "A",
    IACSGrainShapeType.FC_SF: "B",
    IACSGrainShapeType.FC_XR: "C",
    IACSGrainShapeType.DH: "f",
    IACSGrainShapeType.DH_CP: "D",
    IACSGrainShapeType.DH_PR: "E",
    IACSGrainShapeType.DH_CH: "F",
    IACSGrainShapeType.DH_LA: "G",
    IACSGrainShapeType.DH_XR: "H",
    IACSGrainShapeType.SH: "g",
    IACSGrainShapeType.SH_SU: "I",
    IACSGrainShapeType.SH_CV: "J",
    IACSGrainShapeType.SH_XR: "K",
    IACSGrainShapeType.MF: "h",
    IACSGrainShapeType.MF_CL: "L",
    IACSGrainShapeType.MF_PC: "M",
    IACSGrainShapeType.MF_SL: "N",
    IACSGrainShapeType.MF_CR: "O",
    IACSGrainShapeType.IF: "i",
    IACSGrainShapeType.IF_IL: "P",
    IACSGrainShapeType.IF_IC: "Q",
    IACSGrainShapeType.IF_BI: "R",
    IACSGrainShapeType.IF_RC: "S",
    IACSGrainShapeType.IF_SC: "T"
}

IACS_HARDNESS_TYPE_DICT = {
    IACSHardnessType.F_MINUS: "TT",
    IACSHardnessType.F: "",
    IACSHardnessType.F_PLUS: "a",
    IACSHardnessType.FF4: "T2",
    IACSHardnessType.F4_MINUS: "2T",
    IACSHardnessType.F4: "2",
    IACSHardnessType.F4_PLUS: "2a",
    IACSHardnessType.F4F1: "23",
    IACSHardnessType.F1_MINUS: "3T",
    IACSHardnessType.F1: "3",
    IACSHardnessType.F1_PLUS: "3a",
    IACSHardnessType.F1P: "34",
    IACSHardnessType.P_MINUS: "4T",
    IACSHardnessType.P: "4",
    IACSHardnessType.P_PLUS: "4a",
    IACSHardnessType.PK: "45",
    IACSHardnessType.K_MINUS: "5T",
    IACSHardnessType.K: "5",
    IACSHardnessType.K_PLUS: "5a",
    IACSHardnessType.KI: "56",
    IACSHardnessType.I_MINUS: "iT",
    IACSHardnessType.I: "i"

}

IACS_LIQUID_WATER_CONTENT_TYPE_DICT = {
    IACSLiquidWaterContentType.D: "",
    IACSLiquidWaterContentType.DM: "T7",
    IACSLiquidWaterContentType.M: "7",
    IACSLiquidWaterContentType.MW: "7T8",
    IACSLiquidWaterContentType.W: "8",
    IACSLiquidWaterContentType.WV: "8T9",
    IACSLiquidWaterContentType.V: "9",
    IACSLiquidWaterContentType.VS: "9T0",
    IACSLiquidWaterContentType.S: "0"

}
