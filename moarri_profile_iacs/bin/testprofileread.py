# -*- coding: utf-8 -*-

__author__ = 'Kuba Radliński'

import sys
import os
from moarri_profile_iacs.iacs_profile.profile_parser import parse_caaml_file
from moarri_profile_iacs.iacs_profile.profile_writer import create_caaml_file

from xml.dom import minidom

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: program caaml_file")
        mydir = os.path.dirname(os.path.abspath(__file__))
        caaml_file = os.path.abspath(os.path.join(mydir, '..', 'test_files', 'Snowprofile_IACS_SLF7245.xml'))
    else:
        caaml_file = sys.argv[1]

    print(caaml_file)
    caaml = parse_caaml_file(minidom.parse(caaml_file))
    print(caaml)
    newdoc = create_caaml_file(caaml)
    print(newdoc.toprettyxml(indent='\t'))