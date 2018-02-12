# -*- coding: utf-8 -*-

import sys
import os
from moarri_profile_iacs.profile_tools.spp import import_spp
from moarri_profile_iacs.iacs_profile.profile_writer import create_caaml_file
__author__ = 'Kuba Radliński'


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