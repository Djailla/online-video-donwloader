#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

ROOT_PATH = "/Users/gid509037/Perso/shares"

path_list = ''.join('<option>%s</option>\n' % os.path.join(ROOT_PATH, folder)
                    for folder in os.listdir(ROOT_PATH)
                    if not folder.startswith('.'))

print path_list
