#-----------------------------------------------------------------------------
# Copyright (c) 2005-2023, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License (version 2
# or later) with exception for distributing the bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#
# SPDX-License-Identifier: (GPL-2.0-or-later WITH Bootloader-exception)
#-----------------------------------------------------------------------------
from PyInstaller.utils.hooks import is_module_satisfies
from PyInstaller.utils.hooks.gi import GiModuleInfo

module_info = GiModuleInfo('GObject', '2.0')
if module_info.available:
    binaries, datas, hiddenimports = module_info.collect_typelib_data()
    # gi._gobject removed from PyGObject in version 3.25.1
    if is_module_satisfies('PyGObject < 3.25.1'):
        hiddenimports += ['gi._gobject']
