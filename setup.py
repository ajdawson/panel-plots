"""Build and install panel-plots."""
# Copyright 2016 Andrew Dawson
#
# This file is part of panel-plots.
#
# panel-plots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# panel-plots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with panel-plots.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)

from setuptools import setup
try:
    import versioneer
except ImportError:
    raise ImportError('versioneer is required to install panel-plots')


# Define the required dependencies:
install_requires = [
    'versioneer',
    'setuptools>=0.7.2'
]

# Define packages and package data:
packages = [
    'panels',
    'panels.tests',
]

setup(
    name='panel-plots',
    version=versioneer.get_version(),
    author="Andrew Dawson",
    url='https://github.com/ajdawson/panel-plots',
    description='Organize matplotlib plots in panels',
    license='GPL3',
    install_requires=install_requires,
    packages=packages,
    cmdclass=versioneer.get_cmdclass(),
)
