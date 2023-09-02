##
##  Copyright (c) 2023 Chakib Ben Ziane <contact@blob42.xyz> . All rights reserved.
##
##  SPDX-License-Identifier: AGPL-3.0-or-later
##
##  This file is part of Instrukt.
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU Affero General Public License as
##  published by the Free Software Foundation, either version 3 of the
##  License, or (at your option) any later version.
## 
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU Affero General Public License for more details.
## 
##  You should have received a copy of the GNU Affero General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
"""Self documenting index for instrukt."""

import os
import shutil
import tempfile

import pkg_resources


def prepare_src(pkg_name):
    """
    Copies the source code of the specified package to a temporary directory.
    It then strips out all copyright notices from the file headers.

    Args:
        pkg_name (str): Name of the package to copy source code from.

    Returns:
        str: The path of the temporary directory where the source code was copied to.
    """
    # Find the package's source files using pkg_resources

    package_dir = pkg_resources.get_distribution(pkg_name).location
    src_files = []

    for root, dirs, files in os.walk(package_dir):
        for file in files:
            if file.endswith('.py'):
                src_files.append(os.path.join(root, file))

    # Create a temporary directory to store the source code
    temp_dir = tempfile.mkdtemp()

    # Copy the source files to the temporary directory
    for src_file in src_files:
        if src_file.endswith(".py"):
            src_path = os.path.join(package_dir, src_file)
            dst_path = os.path.join(temp_dir, os.path.basename(src_file))
            shutil.copy(src_path, dst_path)

    # Strip out copyright notices from file headers
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)

                with open(file_path, "r+") as f:
                    lines = f.readlines()
                    f.seek(0)

                    # Find the first non-## line (i.e. docstring or python code)
                    for i, line in enumerate(lines):
                        if not line.startswith("##"):
                            break

                # Write all lines from the first non-## line to the end of the file
                f.writelines(lines[i:])
                f.truncate()

    return temp_dir
