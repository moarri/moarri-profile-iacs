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
from moarri_profile_iacs.iacs_profile.profile_parser import parse_caaml_file
from moarri_profile_iacs.iacs_graphics.profile_image import ProfileGraphicsImage
from xml.dom import minidom


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: program caaml_file")
        mydir = os.path.dirname(os.path.abspath(__file__))
        # caaml_file = os.path.abspath(os.path.join(mydir, '..', 'test_files', 'Snowprofile_IACS_SLF7245.xml'))
        caaml_file = os.path.abspath(os.path.join(mydir, '..', 'test_files', 'markowe.xml'))
        image_file = 'C:/TEMP/pil-profile-test.png'
    elif len(sys.argv) < 3:
        image_file = 'C:/TEMP/pil-profile-test.png'
    else:
        caaml_file = sys.argv[1]
        image_file = sys.argv[2]

    print(caaml_file)
    snow_profile = parse_caaml_file(caaml_file)
    print(snow_profile)
    profileImage = ProfileGraphicsImage(snow_profile, 800, 620)
    profileImage.maxSnowHeight = 300
    profileImage.boottomOfGraph = 80
    profileImage.draw_graph()
    profileImage.image.save(image_file, 'PNG')
