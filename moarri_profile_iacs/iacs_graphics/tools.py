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


def draw_centered_string(graphics, xy, txt, color, fnt):
    if len(txt)>0:
        size = fnt.getsize(txt)
        graphics.text((xy[0] - int(size[0] / 2), xy[1] - int(size[1] / 2)), txt, fill=color, font=fnt)
