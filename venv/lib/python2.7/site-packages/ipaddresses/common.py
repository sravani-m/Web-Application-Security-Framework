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

"""Common use constants and functions."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import imp
import io  # Python 3 compatibility
import json
import os
import pickle as pkl
import sys
import time

# from builtins import input  # Python 3 compatibility

import appinfo
import localization as lcl


APP_INFO_FILENAME = 'appinfo.py'

PY = int(sys.version[0])

# set correct path to all data files
DATA_PATH = ''
# if current module is frozen, use exe path
if (hasattr(sys, 'frozen') or  # new py2exe
   hasattr(sys, 'importers') or  # old py2exe
   imp.is_frozen('__main__')):  # tools/freeze
    DATA_PATH = os.path.dirname(sys.executable.decode(lcl.UTF_ENC)) + os.sep
else:
    # use ...\site-packages\XXXXX\
    DATA_PATH = os.path.dirname(__file__) + os.sep

PKL = 0
JSON = 1
FILE_EXT = {JSON: '.json', PKL: '.pkl'}

DATA_FORMAT = JSON

DATA_FILE = DATA_PATH + 'data' + FILE_EXT[DATA_FORMAT]

LOG_FILE = DATA_PATH + 'log' + FILE_EXT[DATA_FORMAT]
LOG = False

LICENSE_FILE = DATA_PATH + 'LICENSE.txt'

if lcl.LANG == 'PT':
    USAGE_FILE = DATA_PATH + 'usage_pt.txt'
else:
    USAGE_FILE = DATA_PATH + 'usage.txt'


def usage():
    """Returns usage text, read from a file."""
    text = ''
    if os.path.isfile(USAGE_FILE):  # if file exists
        with io.open(USAGE_FILE, encoding=lcl.FS_ENC) as f_in:
            text = f_in.read()
    else:
        print(lcl.FILE_NOT_FOUND, USAGE_FILE)
    return text


def banner():
    """Returns banner text."""
    banner_txt = '\n' + appinfo.APP_NAME + lcl.VERSION_WITH_SPACES + \
                 appinfo.APP_VERSION + ', ' + appinfo.COPYRIGHT + '\n' + \
                 appinfo.APP_NAME + lcl.BANNER
    return banner_txt


def version():
    """Returns version."""
    return appinfo.APP_VERSION


def license_():
    """Returns license text, read from a file."""
    text = ''
    if os.path.isfile(LICENSE_FILE):  # if file exists
        with io.open(LICENSE_FILE, encoding=lcl.FS_ENC) as f_in:
            text = f_in.read()
    else:
        print(lcl.FILE_NOT_FOUND, LICENSE_FILE)
    return text


def sleep(seconds=5):
    """Pause for specified time."""
    time.sleep(seconds)


def load_data(filename=DATA_FILE):
    """Load data (list)."""
    data_lst = []
    if os.path.isfile(filename):  # if file exists
        if DATA_FORMAT == JSON:
            with io.open(filename, encoding=lcl.UTF_ENC) as f_in:
                data_lst = json.loads(f_in.read())
        elif DATA_FORMAT == PKL:
            with open(filename, 'rb') as f_in:
                if PY < 3:
                    data_lst = pkl.load(f_in)
                else:
                    data_lst = pkl.load(f_in, encoding='bytes')
        else:
            # error
            pass
    else:
        print(lcl.FILE_NOT_FOUND, filename)
    return data_lst


def save_data(data_lst, filename=DATA_FILE):
    """Save data (list)."""
    if DATA_FORMAT == JSON:
        with io.open(filename, 'w', encoding=lcl.UTF_ENC) as f_out:
            f_out.write(json.dumps(data_lst, ensure_ascii=False))
    elif DATA_FORMAT == PKL:
        with open(filename, 'wb') as f_out:
            pkl.dump(data_lst, f_out, protocol=2)  # max protocol btw Py2 & Py3
    else:
        # error
        pass


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
