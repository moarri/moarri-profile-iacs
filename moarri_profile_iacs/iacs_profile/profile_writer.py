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

from moarri_profile_iacs.iacs_profile.iacs_caaml_meta import *
from moarri_profile_iacs.iacs_profile.iacs_caaml_types import *
from xml.dom.minidom import Document


def _create_value_uom_node(document, node_name, node_value, node_uom):
    node = document.createElement(node_name.code)
    node.setAttribute(ATTR_UOM, node_uom.code)
    node.appendChild(document.createTextNode(node_value.code if isinstance(node_value, CodeableEnum) else str(node_value)))
    return node


def _create_value_node(document, node_name, node_value):
    node = document.createElement(node_name.code)
    node.appendChild(document.createTextNode(node_value.code if isinstance(node_value, CodeableEnum) else str(node_value)))
    return node


def _create_aspect_node(document, aspect):
    aspect_node = document.createElement(AspectMeta.MAIN_NODE.code)
    aspect_node.appendChild(_create_value_node(document, AspectMeta.CHILD_POSITION, aspect.aspect_position))
    return aspect_node


def _create_wind_dir_node(document, wind_dir):
    wind_dir_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_WIND_DIR.code)
    wind_dir_node.appendChild(_create_aspect_node(document, wind_dir))
    return wind_dir_node


def _create_comment_node(document, comment):
    comment_str = comment if comment is not None else ''
    comment_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_COMMENT.code)
    comment_node.appendChild(document.createTextNode(comment_str))
    return comment_node


def _create_snow_height_components_node(document, shc):
    shc_node = document.createElement(SnowHeightComponentsMeta.MAIN_NODE.code)
    if shc.components_type == SnowHeightComponentsType.BOTH or shc.components_type == SnowHeightComponentsType.SNOW_HEIGHT:
        shc_node.appendChild(_create_value_uom_node(document, SnowHeightComponentsMeta.CHILD_SNOW_HEIGHT, shc.snow_height, shc.snow_height_uom))
    if shc.components_type == SnowHeightComponentsType.BOTH or shc.components_type == SnowHeightComponentsType.WATER_EQUIWALENT:
        shc_node.appendChild(_create_value_uom_node(document, SnowHeightComponentsMeta.CHILD_SWE, shc.swe, shc.swe_uom))
    return shc_node


def _create_height_of_snowpack_node(document, shc):
    hs_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_HS.code)
    hs_node.appendChild(_create_snow_height_components_node(document, shc))
    return hs_node


def _create_24h_new_snow_node(document, shc):
    new_snow_24_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_HN24.code)
    new_snow_24_node.appendChild(_create_snow_height_components_node(document, shc))
    return new_snow_24_node


def _create_irregular_interwal_new_snow_node(document, shc):
    irregular_interwal_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_HIN.code)
    irregular_interwal_node.appendChild(_create_snow_height_components_node(document, shc))
    return irregular_interwal_node


def _create_temp_obs_node(document,temp_obs):
    obs_node = document.createElement(TempProfileObsMeta.MAIN_NODE.code)
    obs_node.appendChild(_create_value_node(document, TempProfileObsMeta.CHILD_DEPTH, temp_obs.depth))
    obs_node.appendChild(_create_value_node(document, TempProfileObsMeta.CHILD_SNOW_TEMP, temp_obs.snow_temp))
    return obs_node


def _create_temp_profile_node(document, temp_profile):
    temp_profile_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_TEMP_PROFILE.code)
    temp_profile_node.setAttribute(UOM_DEPTH,temp_profile.temp_profile_uom_depth.code)
    temp_profile_node.setAttribute(UOM_TEMP,temp_profile.temp_profile_uom_temp.code)
    for obs in [_create_temp_obs_node(document, x) for x in temp_profile.temp_profile]:
        temp_profile_node.appendChild(obs)
    return temp_profile_node


def _create_grain_size_node(document,grain_size):
    grain_size_node = document.createElement(LayerMeta.CHILD_GRAIN_SIZE.code);
    grain_size_node.setAttribute(ATTR_UOM,grain_size.uom.code)
    grain_size_elements = document.createElement(GrainSizeMeta.MAIN_NODE.code);
    if grain_size.avg is not None:
        grain_size_elements.appendChild(_create_value_node(document, GrainSizeMeta.CHILD_AVG, grain_size.avg.double_value if grain_size.avg.grain_size_type == CompositeValueType.NUMERIC else grain_size.avg.cardinal_value))
    if grain_size.avg_max is not None:
        grain_size_elements.appendChild(_create_value_node(document, GrainSizeMeta.CHILD_AVG_MAX, grain_size.avg_max.double_value if grain_size.avg_max.grain_size_type == CompositeValueType.NUMERIC else grain_size.avg_max.cardinal_value))
    grain_size_node.appendChild(grain_size_elements)
    return grain_size_node


def _create_layer_node(document, layer):
    layer_node = document.createElement(LayerMeta.MAIN_NODE.code)
    layer_node.appendChild(_create_value_uom_node(document, LayerMeta.CHILD_DEPTH_TOP, layer.depth_top, layer.depth_top_uom))
    layer_node.appendChild(_create_value_uom_node(document, LayerMeta.CHILD_THICKNESS, layer.thickness, layer.thickness_uom))
    if layer.grain_form_primary is not None:
        layer_node.appendChild(_create_value_node(document, LayerMeta.CHILD_GRAIN_FORM_PRIMARY, layer.grain_form_primary))
    if layer.grain_form_secondary is not None:
        layer_node.appendChild(_create_value_node(document, LayerMeta.CHILD_GRAIN_FORM_SECONDARY, layer.grain_form_secondary))
    if layer.grain_size is not None:
        layer_node.appendChild(_create_grain_size_node(document,layer.grain_size))
    if layer.hardness is not None:
        layer_node.appendChild(_create_value_uom_node(document, LayerMeta.CHILD_HARDNESS, layer.hardness.cardinal_value if layer.hardness.hardness_type == CompositeValueType.CARDINAL else layer.hardness.double_value, layer.hardness.uom))
    if layer.lwc is not None:
        layer_node.appendChild(_create_value_uom_node(document, LayerMeta.CHILD_LWC, layer.lwc.cardinal_value if layer.lwc.lwc_type == CompositeValueType.CARDINAL else layer.lwc.double_value, layer.lwc.uom))
    return layer_node


def _create_strat_profile_node(document, strat_profile):
    strat_profile_node = document.createElement(SnowProfileMeasurementsMeta.CHILD_STRAT_PROFILE.code)
    if strat_profile is not None and len(strat_profile) > 0:
        for layer in [_create_layer_node(document, x) for x in strat_profile]:
            strat_profile_node.appendChild(layer)
    return strat_profile_node


def _create_measurements_node(document, measurements):
    measurements_node = document.createElement(SnowProfileMeasurementsMeta.MAIN_NODE.code)
    measurements_node.appendChild(_create_comment_node(document, measurements.comment))
    measurements_node.setAttribute(SnowProfileMeasurementsMeta.ATTR_DIR.code, IACSDirectionType.value_of(measurements.direction))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_PROFILE_DEPTH, measurements.profile_depth, measurements.profile_depth_uom))
    measurements_node.appendChild(_create_value_node(document, SnowProfileMeasurementsMeta.CHILD_SKY_COND, measurements.sky_cond))
    measurements_node.appendChild(_create_value_node(document, SnowProfileMeasurementsMeta.CHILD_PRECIP_TI, measurements.precip_ti))
    measurements_node.appendChild(_create_wind_dir_node(document, measurements.wind_dir))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_PENETRATION_RAM, measurements.penetration_ram, measurements.penetration_ram_uom))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_PENETRATION_FOOT, measurements.penetration_foot, measurements.penetration_foot_uom))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_PENETRATION_SKI, measurements.penetration_ski, measurements.penetration_ski_uom))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_AIR_TEMP_PRES, measurements.air_temp_pres, measurements.air_temp_pres_uom))
    measurements_node.appendChild(_create_value_uom_node(document, SnowProfileMeasurementsMeta.CHILD_WIND_SPD, measurements.wind_spd, measurements.wind_spd_uom))
    if measurements.hs is not None:
        measurements_node.appendChild(_create_height_of_snowpack_node(document, measurements.hs))
    if measurements.hn24 is not None:
        measurements_node.appendChild(_create_24h_new_snow_node(document, measurements.hn24))
    if measurements.hin is not None:
        measurements_node.appendChild(_create_irregular_interwal_new_snow_node(document, measurements.hin))
    if measurements.temp_profile is not None:
        measurements_node.appendChild( _create_temp_profile_node(document, measurements.temp_profile))
    measurements_node.appendChild(_create_strat_profile_node(document, measurements.strat_profile))
    return measurements_node

def _create_results_node(document, results):
    results_node = document.createElement(SnowProfileMeta.CHILD_SNOW_PROFILE_RESULTS_OF.code)
    if results.measurements is not None:
       meas_node  = _create_measurements_node(document,results.measurements)
       if meas_node is not None:
           results_node.appendChild(meas_node)


    return results_node


def _create_snow_profile_node(document, profile):
    profile_node = document.createElement(SnowProfileMeta.MAIN_NODE.code)
    profile_node.setAttribute(SnowProfileMeta.ATTR_XMLNS.code, SnowProfileMeta.ATTR_XMLNS_VALUE.code)
    profile_node.setAttribute(SnowProfileMeta.ATTR_XMLNS_GML.code, SnowProfileMeta.ATTR_XMLNS_GML_VALUE.code)
    profile_node.setAttribute(SnowProfileMeta.ATTR_XMLNS_APP.code, SnowProfileMeta.ATTR_XMLNS_APP_VALUE.code)
    profile_node.setAttribute(SnowProfileMeta.ATTR_XMLNS_XSI.code, SnowProfileMeta.ATTR_XMLNS_XSI_VALUE.code)
    profile_node.setAttribute(SnowProfileMeta.ATTR_XSI_SCHEMA_LOCATION.code, SnowProfileMeta.ATTR_XSI_SCHEMA_LOCATION_VALUE.code)
    if profile.profile_id is not None:
        profile_node.setAttribute(SnowProfileMeta.ATTR_GML_ID.code, profile.profile_id)
    if profile.results is not None:
        profile_node.appendChild(_create_results_node(document, profile.results))
    return profile_node


def create_caaml_file(profile):
    xmldoc = Document()
    xmldoc.version = '1.0'
    xmldoc.encoding = u'UTF-8'
    xmldoc.appendChild(_create_snow_profile_node(xmldoc, profile))
    return xmldoc
