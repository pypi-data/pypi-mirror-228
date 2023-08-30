#-----------------------------------------------------------------------------
# Copyright (c) 2013-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------

# This file is part of the package for testing eggs in `PyInstaller`.

from setuptools import setup

setup(
    name='zipped_egg',
    version='0.1',
    description='A zipped egg for testing PyInstaller',
    packages=['zipped_egg'],
    package_data={'zipped_egg': ['data/datafile.txt']},
)
