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

from PyInstaller.utils.hooks.qt import add_qt5_dependencies, pyqt5_library_info

hiddenimports, binaries, datas = add_qt5_dependencies(__file__)
binaries += pyqt5_library_info.collect_qtnetwork_files()
