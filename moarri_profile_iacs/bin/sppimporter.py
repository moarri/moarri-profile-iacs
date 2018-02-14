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
from moarri_profile_iacs.profile_tools.spp import import_spp
from moarri_profile_iacs.iacs_profile.profile_writer import create_caaml_file


DEFAULT_OUTPUT_FILE = 'C:/TEMP/test-spp-import.xml'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: program spp_file")
        mydir = os.path.dirname(os.path.abspath(__file__))
        quit(1)
    elif len(sys.argv) < 3:
        caaml_file = 'C:/TEMP/test-spp-import.xml'
    else:
        spp_file = sys.argv[1]
        caaml_file = sys.argv[2]

    profile = import_spp(spp_file)
    profile_doc = create_caaml_file(profile)
    with open(caaml_file,'w') as of:
        profile_doc.writexml(of)