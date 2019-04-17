#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Application basic information."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
# import io  # Python 3 compatibility

# from builtins import input  # Python 3 compatibility


APP_NAME = 'ipaddresses'
APP_VERSION = '0.0.2'
APP_LICENSE = 'GNU General Public License v2 or later (GPLv2+)'
APP_AUTHOR = 'Joao Carlos Roseta Matos'
APP_EMAIL = 'jcrmatos@gmail.com'
APP_URL = 'https://github.com/jcrmatos/ipaddresses'
APP_KEYWORDS = 'ip address private public'

# change classifiers to be correct for your application/module
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Environment :: MacOS X',
               'Environment :: Other Environment',
               'Environment :: Win32 (MS Windows)',
               'Environment :: X11 Applications',
               'Intended Audience :: End Users/Desktop',
               'License :: OSI Approved ::' + ' ' + APP_LICENSE,
               'Natural Language :: English',
               'Natural Language :: Portuguese',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.4',
               'Topic :: System :: Networking']

COPYRIGHT = 'Copyright 2009-' + str(dt.date.today().year) + ' ' + APP_AUTHOR

APP_TYPE = 'application'  # it can be application or module

README_FILE = 'README.rst'
REQUIREMENTS_FILE = 'requirements.txt'
