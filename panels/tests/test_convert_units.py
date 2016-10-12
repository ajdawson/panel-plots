"""Tests for unit conversions."""
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

from hypothesis import assume, given

from panels._units import convert_units
from panels.tests import almost_equal, offset_st, unit_st


@given(value=offset_st, units=unit_st)
def test_identity(value, units):
    """Converting to the same unit is the identity."""
    converted = convert_units(value, units, units)
    assert converted == value


@given(value=offset_st, source_units=unit_st, target_units=unit_st)
def test_roundtrip(value, source_units, target_units):
    """Round-trip conversion should not change the value."""
    converted = convert_units(value, source_units, target_units)
    round_tripped = convert_units(converted, target_units, source_units)
    assert almost_equal(round_tripped, value)


@given(value=offset_st)
def test_mm_greater_than_cm(value):
    """A given length is greater measured in mm than in cm."""
    assume(value > 0)
    converted = convert_units(value, 'mm', 'cm')
    assert value > converted


@given(value=offset_st)
def test_mm_greater_than_inches(value):
    """A given length is greater measured in mm than in inches."""
    assume(value > 0)
    converted = convert_units(value, 'mm', 'inches')
    assert value > converted


@given(value=offset_st)
def test_cm_greater_than_inches(value):
    """A given length is greater measured in cm than in inches."""
    assume(value > 0)
    converted = convert_units(value, 'cm', 'inches')
    assert value > converted


@given(value=offset_st)
def test_cm_less_than_mm(value):
    """A given length is less measured in cm than in mm."""
    assume(value > 0)
    converted = convert_units(value, 'cm', 'mm')
    assert value < converted


@given(value=offset_st)
def test_inches_less_than_mm(value):
    """A given length is less measured in inches than in mm."""
    assume(value > 0)
    converted = convert_units(value, 'inches', 'mm')
    assert value < converted


@given(value=offset_st)
def test_inches_less_than_cm(value):
    """A given length is less measured in inches than in cm."""
    assume(value > 0)
    converted = convert_units(value, 'inches', 'cm')
    assert value < converted
