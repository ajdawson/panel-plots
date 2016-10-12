"""Unit conversions for measurements of length."""
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


def convert_units(quantity, source_units, target_units):
    """
    Convert a quantity from one unit of length to another. Supported
    units of length are 'mm', 'cm', and 'inches'.

    Arguments:

    * quantity: numeric
        The quantity to convert.

    * source_units: string
        The units of `quantity`.

    * target_units: string
        The desired units of the output.

    Returns:

    * qn: numeric
        The quantity converted to the units given by `target_units`.

    """
    source_units = _normalize_units(source_units)
    target_units = _normalize_units(target_units)
    if source_units == target_units:
        return quantity
    try:
        converters_from_source_units = _CONVERSIONS[source_units]
    except KeyError:
        raise
    try:
        converter = converters_from_source_units[target_units]
    except KeyError:
        raise
    return converter(quantity)


def _normalize_units(units):
    """
    Convert units to normalized form.

    Converts to lower case and if necessary applies one of the following
    transforms:

        millim[.]* -> mm
        centim[.]* -> cm
        inch[.]*   -> inches

    """
    normed = units.lower()
    if normed.startswith('inch'):
        normed = 'inches'
    elif normed.startswith('millim'):
        normed = 'mm'
    elif normed.startswith('centim'):
        normed = 'cm'
    return normed


#: Conversion functions to go between the three units of length.
_CONVERSIONS = {
    'mm': {'cm': lambda mm: mm / 10,
           'inches': lambda mm: mm / 25.4},
    'cm': {'mm': lambda cm: cm * 10,
           'inches': lambda cm: (cm * 10) / 25.4},
    'inches': {'mm': lambda inches: inches * 25.4,
               'cm': lambda inches: inches * 25.4 / 10},
}
