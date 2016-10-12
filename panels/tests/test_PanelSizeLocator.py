"""Tests for `panels.PanelSizeLocator`."""
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

from hypothesis import given
import pytest

from panels import PanelSizeLocator
from panels.tests import (check_panels_in_figure, gridsize_st, length_st,
                          offset_st)


#: Length units to generate test cases for.
TEST_UNITS = ['mm', 'cm', 'inches']


#-----------------------------------------------------------------------
# Tests default positioning.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st)
def test_defaults(rows, columns, panelwidth, panelheight):
    """All default settings."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight)
    figwidth, figheight = l.figsize_in('mm')
    assert figwidth == panelwidth * columns
    assert figheight == panelheight * rows
    check_panels_in_figure(l)


@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st)
def test_default_positioning(rows, columns, panelwidth, panelheight, units):
    """Default positioning settings with specified units."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert l.rows == rows
    assert l.columns == columns
    assert figwidth == panelwidth * columns
    assert figheight == panelheight * rows
    check_panels_in_figure(l)


#-----------------------------------------------------------------------
# Tests with horizontal and vertical separation.
#-----------------------------------------------------------------------

@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, hsep=offset_st)
def test_with_hsep(rows, columns, panelwidth, panelheight, hsep, units):
    """Positioning with horizontal separation."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         hsep=hsep, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == hsep * (columns - 1) + columns * panelwidth
    assert figheight == rows * panelheight
    check_panels_in_figure(l)


@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, vsep=offset_st)
def test_with_vsep(rows, columns, panelwidth, panelheight, vsep, units):
    """Positioning with vertical separation."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         vsep=vsep, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == columns * panelwidth
    assert figheight == vsep * (rows - 1) + rows * panelheight
    check_panels_in_figure(l)


@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, hsep=offset_st, vsep=offset_st)
def test_with_hsep_and_vsep(rows, columns, panelwidth, panelheight,
                            hsep, vsep, units):
    """Positioning with horizontal and vertical separation."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         hsep=hsep, vsep=vsep, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == hsep * (columns - 1) + columns * panelwidth
    assert figheight == vsep * (rows - 1) + rows * panelheight
    check_panels_in_figure(l)


#-----------------------------------------------------------------------
# Tests with padding.
#-----------------------------------------------------------------------

@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, padleft=offset_st)
def test_with_padleft(rows, columns, panelwidth, panelheight, padleft, units):
    """Positioning with left side padding."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         padleft=padleft, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == columns * panelwidth + padleft
    assert figheight == rows * panelheight
    check_panels_in_figure(l)


@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, padright=offset_st)
def test_with_padright(rows, columns, panelwidth, panelheight, padright,
                       units):
    """Positioning with right side padding."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         padright=padright, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == columns * panelwidth + padright
    assert figheight == rows * panelheight
    check_panels_in_figure(l)


@pytest.mark.parametrize("units", TEST_UNITS)
@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, padtop=offset_st)
def test_with_padtop(rows, columns, panelwidth, panelheight, padtop, units):
    """Positioning with top edge padding."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         padtop=padtop, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == columns * panelwidth
    assert figheight == rows * panelheight + padtop
    check_panels_in_figure(l)


@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, padbottom=offset_st)
@pytest.mark.parametrize("units", TEST_UNITS)
def test_with_padbottom(rows, columns, panelwidth, panelheight, padbottom,
                        units):
    """Positioning with bottom edge padding."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         padbottom=padbottom, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == columns * panelwidth
    assert figheight == rows * panelheight + padbottom
    check_panels_in_figure(l)


@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, padleft=offset_st, padright=offset_st,
       padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize("units", TEST_UNITS)
def test_with_pad(rows, columns, panelwidth, panelheight, padleft, padright,
                  padtop, padbottom, units):
    """Positioning with padding on all sides."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         padleft=padleft, padright=padright,
                         padtop=padtop, padbottom=padbottom, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == padleft + columns * panelwidth + padright
    assert figheight == padtop + rows * panelheight + padbottom
    check_panels_in_figure(l)


#-----------------------------------------------------------------------
# Tests with both padding and separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, panelwidth=length_st,
       panelheight=length_st, hsep=offset_st, vsep=offset_st,
       padleft=offset_st, padright=offset_st, padtop=offset_st,
       padbottom=offset_st)
@pytest.mark.parametrize("units", TEST_UNITS)
def test_with_pad_and_sep(rows, columns, panelwidth, panelheight, hsep, vsep,
                          padleft, padright, padtop, padbottom, units):
    """Positioning with both padding and separation."""
    l = PanelSizeLocator(rows, columns, panelwidth, panelheight,
                         hsep=hsep, vsep=vsep,
                         padleft=padleft, padright=padright,
                         padtop=padtop, padbottom=padbottom, units=units)
    figwidth, figheight = l.figsize_in(units)
    assert figwidth == (padleft + columns * panelwidth +
                        (columns - 1) * hsep + padright)
    assert figheight == (padtop + rows * panelheight +
                         (rows - 1) * vsep + padbottom)
    check_panels_in_figure(l)
