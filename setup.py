#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup file of Janitoo
"""
__license__ = """
    This file is part of Janitoo.

    Janitoo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Janitoo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Janitoo. If not, see <http://www.gnu.org/licenses/>.

"""
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'
__copyright__ = "Copyright © 2013-2014 Sébastien GALLET aka bibi21000"

from os import name as os_name
from setuptools import setup, find_packages
from distutils.extension import Extension
from platform import system as platform_system
import glob
import os
import sys
from _version import janitoo_version

DEBIAN_PACKAGE = False
filtered_args = []

for arg in sys.argv:
    if arg == "--debian-package":
        DEBIAN_PACKAGE = True
    else:
        filtered_args.append(arg)
sys.argv = filtered_args

def data_files_config(res, rsrc, src, pattern):
    for root, dirs, fils in os.walk(src):
        if src == root:
            sub = []
            for fil in fils:
                sub.append(os.path.join(root,fil))
            res.append((rsrc, sub))
            for dire in dirs:
                    data_files_config(res, os.path.join(rsrc, dire), os.path.join(root, dire), pattern)

data_files = []
data_files_config(data_files, 'templates','src/janitoo_manager/templates/','*')
data_files_config(data_files, 'themes','src/janitoo_manager/themes/','*')
data_files_config(data_files, 'static','src/janitoo_manager/static/','*')
data_files_config(data_files, 'docs','src/docs/','*')
data_files_config(data_files, 'config','src/config','*.py')
data_files_config(data_files, 'config','src/config','*.conf')
data_files_config(data_files, 'config','src/config','*.mako')
data_files_config(data_files, 'config','src/config','README')

setup(
    name = 'janitoo_manager',
    description = "Janitoo manager",
    long_description = "manager",
    author='Sébastien GALLET aka bibi2100 <bibi21000@gmail.com>',
    author_email='bibi21000@gmail.com',
    license = """
        This file is part of Janitoo.

        Janitoo is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        Janitoo is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with Janitoo. If not, see <http://www.gnu.org/licenses/>.
    """,
    url='http://bibi21000.gallet.info/',
    version = janitoo_version,
    scripts=['src/scripts/jnt_webman'],
    keywords = "admin",
    zip_safe = False,
    include_package_data=True,
    data_files = data_files,
    packages = find_packages('src', exclude=["scripts", "docs", "config"]),
    package_dir = { '': 'src' },
    install_requires=[
                    'janitoo_flask',
                    'janitoo_flask_socketio',
                    'Flask-Mail',
                    'Flask-DebugToolbar',
                    'Flask-Login',
                    'Flask-Script',
                    'Flask-WTF',
                    'MarkupSafe',
                    'Flask-Themes2',
                    'Flask-BabelEx',
                    'requests',
                    'Unidecode',
                    'mistune',
                    ],
    dependency_links = [
      'https://github.com/bibi21000/janitoo_flask/archive/master.zip#egg=janitoo_flask',
      'https://github.com/bibi21000/janitoo_flask_socketio/archive/master.zip#egg=janitoo_flask_socketio',
      'https://github.com/sysr-q/flask-themes2/archive/master.zip#egg=Flask-Themes2',
      'https://github.com/sh4nks/flask-babelex/tarball/master#egg=Flask-BabelEx',
    ],
    entry_points = {
        'janitoo_manager.network': [
            'manager = janitoo_manager.network:extend',
        ],
    }
)
