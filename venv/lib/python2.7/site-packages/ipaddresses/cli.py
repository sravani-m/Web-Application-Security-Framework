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

"""Processes command line arguments."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# import io  # Python 3 compatibility
import sys

from builtins import input  # Python 3 compatibility
import colorama as ansi

import common
import localization as lcl
import shared as shrd


def print_ips():
    """Print private and public IP."""
    print(lcl.PRIVATE_IP + shrd.get_private_ip())
    print(lcl.PUBLIC_IP + shrd.get_public_ip())


def start(argv):
    """Print banner and process args."""
    ansi.init()

    print(common.banner())

    if not argv:
        print_ips()
    else:
        arg0 = argv[0]
        if arg0 in ['-h', '--help']:
            print(common.usage())
        elif arg0 in ['-l', '--license']:
            print(common.license_())
        elif arg0 in ['-p', '--pause']:
            print_ips()
            input(lcl.PRESS_ANY_KEY)
        elif arg0 in ['-V', '--version']:
            print(lcl.VERSION, common.version())
        else:
            print(ansi.Fore.RED + lcl.WRONG_ARG + arg0 + '\n')
            print(ansi.Fore.RESET + common.usage())

    sys.exit(0)  # ToDo: other return codes


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
