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

"""Shared constants and functions between CLI and GUI modules."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

# import io  # Python 3 compatibility
import socket

# from builtins import input  # Python 3 compatibility
from future.moves.urllib.request import urlopen  # Python 3 compatibility


def get_private_ip():
    """Get private IP address."""
    return socket.gethostbyname(socket.gethostname())


def get_public_ip():
    """Get public IP address."""
    data = str(urlopen('http://www.realip.info/api/p/realip.php').read())
    return data.split('"')[3]


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
