# -*- coding: utf-8 -*-

import sys
import os
from moarri_profile_iacs.iacs_profile.profile_parser import parse_caaml_file
from PIL import ImageColor
from moarri_profile_iacs.iacs_graphics.profile_image import ProfileGraphicsImage
from xml.dom import minidom

__author__ = 'Kuba Radliński'


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
    snow_profile = parse_caaml_file(minidom.parse(caaml_file))
    print(snow_profile)
    profileImage = ProfileGraphicsImage(snow_profile, 800, 620)
    profileImage.maxSnowHeight = 300
    profileImage.boottomOfGraph = 80
    profileImage.draw_graph()
    profileImage.image.save(image_file, 'PNG')
