"""Test utilities for panel-plots testing."""
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

from hypothesis.strategies import integers, floats, sampled_from


#: A stretegy to generate positive integers representing grid sizes.
gridsize_st = integers(min_value=1, max_value=100)

#: A strategy to generate lengths (e.g. for panel/figure sizes).
length_st = floats(min_value=1e-5, max_value=1e5, allow_nan=False,
                   allow_infinity=False)

#: A strategy to generate offsets (e.g. for padding or separation).
offset_st = floats(min_value=0, max_value=1e5, allow_nan=False,
                   allow_infinity=False)

#: A strategy to generate units of length.
unit_st = sampled_from(('mm', 'cm', 'inches'))


def almost_equal(a, b, rtol=1e-5, atol=1e-8):
    """
    Check if two numeric values are almost equal.

    """
    return abs(a - b) < (rtol * b + atol)


def check_panels_in_figure(locator):
    """
    Check that every panel produced by a locator is within the figure.

    """
    for (x, y, w, h) in locator.panel_position_iterator():
        assert x >= 0 or almost_equal(x, 0)
        assert y >= 0 or almost_equal(y, 0)
        assert (x + w) <= 1 or almost_equal(x + w, 1)
        assert (y + h) <= 1 or almost_equal(y + h, 1)
