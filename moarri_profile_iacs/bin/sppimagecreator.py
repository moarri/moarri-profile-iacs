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

import sys
import os
import fnmatch

from moarri_profile_iacs.iacs_graphics.profile_image import ProfileGraphicsImage
from moarri_profile_iacs.profile_tools.spp import import_spp


DEFAULT_OUTPUT_FILE = 'C:/TEMP/test-spp-import.xml'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: program spp_file")
        mydir = os.path.dirname(os.path.abspath(__file__))
        quit(1)

    spp_path = sys.argv[1]
    image_path = sys.argv[2]
    snow_profiles = []
    if os.path.isdir(spp_path):
        if not os.path.isdir(image_path):
            print("If source is dir the destination should be directory also")
            quit(1)
        for spp_file_name in fnmatch.filter(os.listdir(spp_path), '*.spp'):
            spp_file = os.path.join(spp_path, spp_file_name)
            image_file = os.path.join(image_path, os.path.splitext(spp_file_name)[0]+'.PNG')
            snow_profiles.append((import_spp(spp_file), spp_file, image_file))
    else:
        snow_profiles.append((import_spp(spp_path), spp_path, image_path))
    unify_snow_heights = False
    snow_profile_height = 0
    if unify_snow_heights:
        snow_profile_height = round(max([sp[0].results.measurements.hs.snow_height for sp in snow_profiles])/10*1.1)*10

    for s in snow_profiles:
        print(s[1], flush=True)
        profileImage = ProfileGraphicsImage(s[0], 800, 620)
        if not unify_snow_heights:
            snow_profile_height = round(s[0].results.measurements.hs.snow_height / 10 * 1.1) * 10
        profileImage.maxSnowHeight = snow_profile_height
        profileImage.boottomOfGraph = 0
        profileImage.draw_graph()
        profileImage.image.save(s[2], 'PNG')
