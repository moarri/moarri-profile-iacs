# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

from iacs_profile.iacs_caaml_profile import *
from xml.dom import Node


def trim_string(x):
    if x is None:
        return None
    return x.strip()


def extract_double(el):
    return float(trim_string(el))


def extract_from_enum_type(enum_cls, el):
    return enum_cls.value_of(trim_string(el))


def extract_unit_attribute(enum_cls, el):
    return enum_cls.value_of(trim_string(el.getAttribute(ATTR_UOM)))


def extract_unit_attribute_name(enum_cls, el, attr_name):
    return enum_cls.value_of(trim_string(el.getAttribute(attr_name)))


def parse_caaml_file(xmldoc):
    snow_profile_node = xmldoc.firstChild
    if not snow_profile_node.localName == SnowProfileMeta.MAIN_NODE.code:
        return None
    else:
        profile_id = snow_profile_node.getAttribute(SnowProfileMeta.ATTR_GML_ID.code)
        results = _parse_snow_profile_results([x for x in snow_profile_node.childNodes if
                                    x.nodeType == Node.ELEMENT_NODE and x.localName == SnowProfileMeta.CHILD_SNOW_PROFILE_RESULTS_OF.code][
            0])
        return SnowProfile(profile_id, results)


def _parse_aspect(e):
    main_node = \
        [x for x in e.childNodes if x.nodeType == Node.ELEMENT_NODE and x.localName == AspectMeta.MAIN_NODE.code][0]
    if main_node is not None and main_node != []:
        position_node = [x for x in main_node.childNodes if
                         x.nodeType == Node.ELEMENT_NODE and x.localName == AspectMeta.CHILD_POSITION.code][0]
        if position_node is not None and position_node != []:
            return Aspect.create_default(extract_from_enum_type(IACSAspectCardinalType, position_node.firstChild.data))
    return None


def _parse_snow_height_components(e):
    components = None
    main_node = [x for x in e.childNodes if
                 x.nodeType == Node.ELEMENT_NODE and x.localName == SnowHeightComponentsMeta.MAIN_NODE.code][0]
    if main_node is not None and main_node != []:
        snow_height = None
        snow_height_uom = None
        swe = None
        swe_uom = None
        height_present = False
        swe_present = False
        for node in [x for x in main_node.childNodes if x.nodeType == Node.ELEMENT_NODE]:
            if node.localName == SnowHeightComponentsMeta.CHILD_SNOW_HEIGHT.code:
                snow_height = extract_double(node.firstChild.data)
                snow_height_uom = extract_unit_attribute(IACSUnitsLengthType, node)
                height_present = True
            elif node.localName == SnowHeightComponentsMeta.CHILD_SWE.code:
                swe = extract_double(node.firstChild.data)
                swe_uom = extract_unit_attribute(IACSUnitsLengthType, node)
                swe_present = True
        if height_present and swe_present:
            components = SnowHeightComponents.create_both(snow_height, snow_height_uom, swe, swe_uom)
        elif height_present:
            components = SnowHeightComponents.create_snow_height(snow_height, snow_height_uom)
        elif swe_present:
            components = SnowHeightComponents.create_swe(swe, swe_uom)
    return components


def _parse_hardness(e):
    force_unit = extract_unit_attribute(IACSUnitsForceType, e)
    if force_unit == IACSUnitsForceType.N:
        hardness = Hardness.create_numeric(extract_double(e.firstChild.data))
    elif force_unit == IACSUnitsForceType.EMPTY:
        hardness = Hardness.create_cardinal(extract_from_enum_type(IACSHardnessType, e.firstChild.data))
    else:
        hardness = Hardness()
    return hardness


def _parse_lwc(e):
    lwc_unit = extract_unit_attribute(IACSUnitsLwcType, e)
    if lwc_unit == IACSUnitsLwcType.PRCVOL:
        lwc = Lwc.create_numeric(extract_double(e.firstChild.data))
    elif lwc_unit == IACSUnitsLwcType.EMPTY:
        lwc = Lwc.create_cardinal(extract_from_enum_type(IACSLiquidWaterContentType, e.firstChild.data))
    else:
        lwc = Lwc()
    return lwc


def _parse_grain_size(e):
    uom = extract_unit_attribute(IACSUnitsLengthType, e)
    main_node = \
        [x for x in e.childNodes if x.nodeType == Node.ELEMENT_NODE and x.localName == GrainSizeMeta.MAIN_NODE.code][0]
    if main_node is None:
        return GrainSize()

    avg = None
    avg_max = None
    for node in [x for x in main_node.childNodes if x.nodeType == Node.ELEMENT_NODE]:
        if node.localName == GrainSizeMeta.CHILD_AVG.code:
            avg = extract_double(node.firstChild.data)
        elif node.localName == GrainSizeMeta.CHILD_AVG_MAX.code:
            avg_max = extract_double(node.firstChild.data)
    return GrainSize.create(uom, avg, avg_max)


def _parse_layer(e):
    depth_top = None
    depth_top_uom = IACSUnitsLengthType.CM
    thickness = None
    thickness_uom = IACSUnitsLengthType.CM
    valid_formation_time = None
    grain_form_primary = None
    grain_form_secondary = None
    grain_size = None
    hardness = None
    lwc = None

    layer_elements = [x for x in e.childNodes if x.nodeType == Node.ELEMENT_NODE]
    for node in layer_elements:
        if node.localName == LayerMeta.CHILD_DEPTH_TOP.code:
            depth_top = extract_double(node.firstChild.data)
            depth_top_uom = extract_unit_attribute(IACSUnitsLengthType, node)
        elif node.localName == LayerMeta.CHILD_THICKNESS.code:
            thickness = extract_double(node.firstChild.data)
            thickness_uom = extract_unit_attribute(IACSUnitsLengthType, node)
        elif node.localName == LayerMeta.CHILD_GRAIN_FORM_PRIMARY.code:
            grain_form_primary = extract_from_enum_type(IACSGrainShapeType, node.firstChild.data)
        elif node.localName == LayerMeta.CHILD_GRAIN_FORM_SECONDARY.code:
            grain_form_secondary = extract_from_enum_type(IACSGrainShapeType, node.firstChild.data)
        elif node.localName == LayerMeta.CHILD_GRAIN_SIZE.code:
            grain_size = _parse_grain_size(node)
        elif node.localName == LayerMeta.CHILD_HARDNESS.code:
            hardness = _parse_hardness(node)
        elif node.localName == LayerMeta.CHILD_LWC.code:
            lwc = _parse_lwc(node)

    return StratProfileLayer(depth_top, depth_top_uom, thickness, thickness_uom, valid_formation_time, grain_form_primary, grain_form_secondary, grain_size, hardness, lwc)


def _parse_strat_profile(e):
    layers = []
    for node in [x for x in e.childNodes if
                 x.nodeType == Node.ELEMENT_NODE and x.localName == LayerMeta.MAIN_NODE.code]:
        layer = _parse_layer(node)
        if layer is not Node:
            layers.append(layer)
    return layers


def _parse_temp_profile_obs(e, depth_uom=IACSUnitsLengthType.CM):
    depth = None
    snow_temp = None
    for node in [x for x in e.childNodes if x.nodeType == Node.ELEMENT_NODE]:
        if node.localName == TempProfileObsMeta.CHILD_DEPTH.code:
            depth = extract_double(node.firstChild.data)
        elif node.localName == TempProfileObsMeta.CHILD_SNOW_TEMP.code:
            snow_temp = extract_double(node.firstChild.data)
    return TempProfileObs(depth, depth_uom, snow_temp)


def _parse_temp_profile(e):
    temp_profile = []
    temp_profile_uom_depth = extract_unit_attribute_name(IACSUnitsLengthType, e, UOM_DEPTH)
    temp_profile_uom_temp = extract_unit_attribute_name(IACSUnitsTempType, e, UOM_TEMP)
    for node in [x for x in e.childNodes if
                 x.nodeType == Node.ELEMENT_NODE and x.localName == TempProfileObsMeta.MAIN_NODE.code]:
        temp_profile_obs = _parse_temp_profile_obs(node, temp_profile_uom_depth)
        if temp_profile_obs is not None:
            temp_profile.append(temp_profile_obs)
    return TempProfile(temp_profile, temp_profile_uom_depth, temp_profile_uom_temp)


def _parse_snow_profile_results(element):
    main_node = [x for x in element.childNodes if
                 x.nodeType == Node.ELEMENT_NODE and x.localName == SnowProfileMeasurementsMeta.MAIN_NODE.code][0]
    if main_node is not None and main_node != []:
        measurement_components = {
            'direction': IACSDirectionType.value_of(main_node.getAttribute(SnowProfileMeasurementsMeta.ATTR_DIR.code))}
        for node in [x for x in main_node.childNodes if x.nodeType == Node.ELEMENT_NODE]:
            if node.localName == SnowProfileMeasurementsMeta.CHILD_COMMENT.code:
                measurement_components['comment'] = trim_string(node.firstChild.data)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_PROFILE_DEPTH.code:
                measurement_components['profile_depth'] = extract_double(node.firstChild.data)
                measurement_components['profile_depth_uom'] = extract_unit_attribute(IACSUnitsLengthType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_PENETRATION_RAM.code:
                measurement_components['penetration_ram'] = extract_double(node.firstChild.data)
                measurement_components['penetration_ram_uom'] = extract_unit_attribute(IACSUnitsLengthType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_PENETRATION_FOOT.code:
                measurement_components['penetration_foot'] = extract_double(node.firstChild.data)
                measurement_components['penetration_foot_uom'] = extract_unit_attribute(IACSUnitsLengthType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_PENETRATION_SKI.code:
                measurement_components['penetration_ski'] = extract_double(node.firstChild.data)
                measurement_components['penetration_ski_uom'] = extract_unit_attribute(IACSUnitsLengthType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_AIR_TEMP_PRES.code:
                measurement_components['air_temp_pres'] = extract_double(node.firstChild.data)
                measurement_components['air_temp_pres_uom'] = extract_unit_attribute(IACSUnitsTempType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_WIND_SPD.code:
                measurement_components['wind_spd'] = extract_double(node.firstChild.data)
                measurement_components['wind_spd_uom'] = extract_unit_attribute(IACSUnitsWindSpdType, node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_WIND_DIR.code:
                aspect = _parse_aspect(node)
                if aspect is not None:
                    measurement_components['wind_dir'] = aspect
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_HS.code:
                components = _parse_snow_height_components(node)
                if components is not None:
                    measurement_components['hs'] = components
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_HIN.code:
                components = _parse_snow_height_components(node)
                if components is not None:
                    measurement_components['hin'] = components
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_HN24.code:
                components = _parse_snow_height_components(node)
                if components is not None:
                    measurement_components['hn24'] = components
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_SKY_COND.code:
                measurement_components['sky_cond'] = extract_from_enum_type(IACSSkyConditionType, node.firstChild.data)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_PRECIP_TI.code:
                measurement_components['precip_ti'] = extract_from_enum_type(IACSPrecipTIType, node.firstChild.data)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_STRAT_PROFILE.code:
                measurement_components['strat_profile'] = _parse_strat_profile(node)
            elif node.localName == SnowProfileMeasurementsMeta.CHILD_TEMP_PROFILE.code:
                measurement_components['temp_profile'] = _parse_temp_profile(node)
    else:
        return None
    results = SnowProfileResults(SnowProfileMeasurements.create_default(**measurement_components))
    return results



