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

import pkg_resources
from unittest import TestCase
from moarri_profile_iacs.iacs_profile.profile_parser import CAAMLProfileIACSVersion, check_caaml_file

_TEST_FILE_V5 = "data/v5/Snowprofile_IACS_SLF7245.xml"
_TEST_FILE_V6 = "data/v6/SnowProfile_IACS_SLF22950.xml"


class TestProfile_parser(TestCase):

    def test_check_caaml_file(self):
        xml_filename = pkg_resources.resource_filename(__name__, _TEST_FILE_V6)
        ok, version = check_caaml_file(xml_filename)
        self.assertTupleEqual((ok, version), (True, 'v6.0.3'), "Shoudl be True, V5")

