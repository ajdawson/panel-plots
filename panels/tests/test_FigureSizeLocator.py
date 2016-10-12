"""Tests for  `panels.FigureSizeLocator`."""
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

from hypothesis import given, assume
import pytest

from panels import FigureSizeLocator
from panels.tests import (almost_equal, gridsize_st, length_st, offset_st)


#: Length units to generate test cases for.
TEST_UNITS = ['mm', 'cm', 'inches']


#-----------------------------------------------------------------------
# Tests specifications (full, width, and height) without padding or
# separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec(rows, columns, figwidth, figheight, units):
    """Full specification (width and height) only."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                          figheight=figheight, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec(rows, columns, figwidth, units):
    """Width specification only."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec(rows, columns, figheight, units):
    """Height specification only."""
    l = FigureSizeLocator(rows, columns, figheight=figheight, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Tests specifications (width and height) with a specified aspect ratio.
#-----------------------------------------------------------------------

@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_ratio_gives_warning(units):
    """Full specification with aspect ratio should generate a warning."""
    expected_msg = ('the "panelratio" keyword is ignored when both the '
                    '"figwidth" and "figheight" keywords are used')
    with pytest.warns(UserWarning) as record:
        l = FigureSizeLocator(1, 1, figwidth=10, figheight=10, panelratio=1,
                              units=units)
    assert len(record) == 1
    assert record[0].message.args[0] == expected_msg


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       panelratio=length_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_ratio(rows, columns, figwidth, panelratio, units):
    """Width specification with aspect ratio."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                          panelratio=panelratio, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c,
                        (figwidth * rows) / (panelratio * columns))


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       panelratio=length_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_ratio(rows, columns, figheight, panelratio, units):
    """Height specification with aspect ratio."""
    l = FigureSizeLocator(rows, columns, figheight=figheight,
                          panelratio=panelratio, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, columns * panelratio * figheight / rows)


#-----------------------------------------------------------------------
# Tests full specifications with horizonal and vertical separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, hsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_hsep(rows, columns, figwidth, figheight, hsep, units):
    """Full specification with horizontal separation."""
    assume(figwidth > hsep * (columns - 1))
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          hsep=hsep, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_vsep(rows, columns, figwidth, figheight, vsep, units):
    """Full specification with vertical separation."""
    assume(figheight > vsep * (rows - 1))
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          vsep=vsep, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, hsep=offset_st, vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_hsep_and_vsep(rows, columns, figwidth, figheight,
                                      hsep, vsep, units):
    """Full specification with horizontal and vertical separation."""
    assume(figwidth > hsep * (columns - 1))
    assume(figheight > vsep * (rows - 1))
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          hsep=hsep, vsep=vsep, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Tests width specifications with horizonal and vertical separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       hsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_hsep(rows, columns, figwidth, hsep, units):
    """Width specification with horizontal separation."""
    assume(figwidth > hsep * (columns - 1))
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, hsep=hsep,
                          units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_vsep(rows, columns, figwidth, vsep, units):
    """Width specification with vertical separation."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, vsep=vsep,
                          units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       hsep=offset_st, vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_hsep_and_vsep(rows, columns, figwidth, hsep, vsep,
                                       units):
    """Width specification with horizontal and vertical separation."""
    assume(figwidth > hsep * (columns - 1))
    l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                          hsep=hsep, vsep=vsep, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


#-----------------------------------------------------------------------
# Tests height specifications with horizonal and vertical separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       hsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_hsep(rows, columns, figheight, hsep, units):
    """Height specification with horizontal separation."""
    l = FigureSizeLocator(rows, columns, figheight=figheight, hsep=hsep,
                          units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_vsep(rows, columns, figheight, vsep, units):
    """Height specification with vertical separation."""
    assume(figheight > vsep * (rows - 1))
    l = FigureSizeLocator(rows, columns, figheight=figheight, vsep=vsep,
                          units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       hsep=offset_st, vsep=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_hsep_and_vsep(rows, columns, figheight, hsep, vsep,
                                        units):
    """Height specification with horizontal and vertical separation."""
    assume(figheight > vsep * (rows - 1))
    l = FigureSizeLocator(rows, columns, figheight=figheight,
                          hsep=hsep, vsep=vsep, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Tests full specifications with padding.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, padleft=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_padleft(rows, columns, figwidth, figheight, padleft,
                                units):
    """Full specification with left side padding."""
    assume(figwidth > padleft)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          padleft=padleft, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, padright=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_padright(rows, columns, figwidth, figheight, padright,
                                 units):
    """Full specification with right side padding."""
    assume(figwidth > padright)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          padright=padright, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, padtop=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_padtop(rows, columns, figwidth, figheight, padtop,
                               units):
    """Full specification with top edge padding."""
    assume(figheight > padtop)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          padtop=padtop, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_padbottom(rows, columns, figwidth, figheight,
                                  padbottom, units):
    """Full specification with bottom edge padding."""
    assume(figheight > padbottom)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          padbottom=padbottom, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, padleft=offset_st, padright=offset_st,
       padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_pad(rows, columns, figwidth, figheight, padleft,
                            padright, padtop, padbottom, units):
    """Full specification with padding on all sides."""
    assume(figwidth > padleft + padright)
    assume(figheight > padbottom + padtop)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          padleft=padleft, padright=padright,
                          padtop=padtop, padbottom=padbottom, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Tests width specifications with padding.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       padleft=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_padleft(rows, columns, figwidth, padleft, units):
    """Width specification with left side padding."""
    assume(figwidth > padleft)
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, padleft=padleft,
                          units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       padright=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_padright(rows, columns, figwidth, padright, units):
    """Width specification with right side padding."""
    assume(figwidth > padright)
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, padright=padright,
                          units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       padtop=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_padtop(rows, columns, figwidth, padtop, units):
    """Width specification with top edge padding."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, padtop=padtop,
                          units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_padbottom(rows, columns, figwidth, padbottom, units):
    """Width specification with bottom edge padding."""
    l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                          padbottom=padbottom, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       padleft=offset_st, padright=offset_st, padtop=offset_st,
       padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_pad(rows, columns, figwidth, padleft, padright,
                             padtop, padbottom, units):
    """Width specification with padding on all sides."""
    assume(figwidth > padleft + padright)
    l = FigureSizeLocator(rows, columns, figwidth=figwidth, padleft=padleft,
                          padright=padright, padtop=padtop,
                          padbottom=padbottom, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


#-----------------------------------------------------------------------
# Tests height specifications with padding.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       padleft=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_padleft(rows, columns, figheight, padleft, units):
    """Height specification with left side padding."""
    l = FigureSizeLocator(rows, columns, figheight=figheight, padleft=padleft,
                          units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       padright=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_padright(rows, columns, figheight, padright, units):
    """Height specification with right side padding."""
    l = FigureSizeLocator(rows, columns, figheight=figheight, padright=padright,
                          units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       padtop=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_padtop(rows, columns, figheight, padtop, units):
    """Height specification with top edge padding."""
    assume(figheight > padtop)
    l = FigureSizeLocator(rows, columns, figheight=figheight, padtop=padtop,
                          units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_padbottom(rows, columns, figheight, padbottom,
                                    units):
    """Height specification with bottom edge padding."""
    assume(figheight > padbottom)
    l = FigureSizeLocator(rows, columns, figheight=figheight,
                          padbottom=padbottom, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       padleft=offset_st, padright=offset_st, padtop=offset_st,
       padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_pad(rows, columns, figheight, padleft, padright,
                              padtop, padbottom, units):
    """Height specification with padding on all sides."""
    assume(figheight > padtop + padbottom)
    l = FigureSizeLocator(rows, columns, figheight=figheight, padleft=padleft,
                          padright=padright, padtop=padtop,
                          padbottom=padbottom, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Test specifications (full, width, and height) with both padding and
# separation.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, hsep=offset_st, vsep=offset_st,
       padleft=offset_st, padright=offset_st, padtop=offset_st,
       padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_with_all(rows, columns, figwidth, figheight, hsep, vsep,
                            padleft, padright, padtop, padbottom, units):
    """Full specification with separation and padding."""
    assume(figwidth > padleft + (columns - 1) * hsep + padright)
    assume(figheight > padtop + (rows - 1) * vsep + padbottom)
    l = FigureSizeLocator(rows, columns,
                          figwidth=figwidth, figheight=figheight,
                          hsep=hsep, vsep=vsep,
                          padleft=padleft, padright=padright,
                          padtop=padtop, padbottom=padbottom, units=units)
    figwidth_c, figheight_c = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)
    assert almost_equal(figheight_c, figheight)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       hsep=offset_st, vsep=offset_st, padleft=offset_st, padright=offset_st,
       padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_with_all(rows, columns, figwidth, hsep, vsep, padleft,
                             padright, padtop, padbottom, units):
    """Width specification with separation and padding."""
    assume(figwidth > padleft + (columns - 1) * hsep + padright)
    l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                          hsep=hsep, vsep=vsep,
                          padleft=padleft, padright=padright,
                          padtop=padtop, padbottom=padbottom, units=units)
    figwidth_c, _ = l.figsize_in(units)
    assert almost_equal(figwidth_c, figwidth)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       hsep=offset_st, vsep=offset_st, padleft=offset_st, padright=offset_st,
       padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_with_all(rows, columns, figheight, hsep, vsep, padleft,
                              padright, padtop, padbottom, units):
    """Height specification with separation and padding."""
    assume(figheight > padtop + (rows - 1) * vsep + padbottom)
    l = FigureSizeLocator(rows, columns, figheight=figheight,
                          hsep=hsep, vsep=vsep,
                          padleft=padleft, padright=padright,
                          padtop=padtop, padbottom=padbottom, units=units)
    _, figheight_c = l.figsize_in(units)
    assert almost_equal(figheight_c, figheight)


#-----------------------------------------------------------------------
# Test error conditions.
#-----------------------------------------------------------------------

@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       figheight=length_st, hsep=offset_st, vsep=offset_st, padleft=offset_st,
       padright=offset_st, padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_full_spec_ill_conditioned(rows, columns, figwidth, figheight, hsep,
                                   vsep, padleft, padright, padtop, padbottom,
                                   units):
    """An error message if the full spec is not large enough."""
    assume (figwidth <= padleft + (columns - 1) * hsep + padright or
            figheight <= padtop + (rows - 1) * vsep + padbottom)
    with pytest.raises(ValueError) as excinfo:
        l = FigureSizeLocator(rows, columns, figwidth=figwidth,
                              figheight=figheight, hsep=hsep, vsep=vsep,
                              padleft=padleft, padright=padright,
                              padtop=padtop, padbottom=padbottom, units=units)
    assert 'not large enough' in str(excinfo.value)


@given(rows=gridsize_st, columns=gridsize_st, figwidth=length_st,
       hsep=offset_st, padleft=offset_st, padright=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_width_spec_ill_conditioned(rows, columns, figwidth, hsep, padleft,
                                    padright, units):
    """An error if the width spec is not large enough."""
    assume (figwidth <= padleft + (columns - 1) * hsep + padright)
    with pytest.raises(ValueError) as excinfo:
        l = FigureSizeLocator(rows, columns, figwidth=figwidth, hsep=hsep,
                              padleft=padleft, padright=padright, units=units)
    assert 'not wide enough' in str(excinfo.value)


@given(rows=gridsize_st, columns=gridsize_st, figheight=length_st,
       vsep=offset_st, padtop=offset_st, padbottom=offset_st)
@pytest.mark.parametrize('units', TEST_UNITS)
def test_height_spec_ill_conditioned(rows, columns, figheight, vsep, padtop,
                                     padbottom, units):
    """An error if the height spec is not large enough."""
    assume (figheight <= padtop + (rows - 1) * vsep + padbottom)
    with pytest.raises(ValueError) as excinfo:
        l = FigureSizeLocator(rows, columns, figheight=figheight, vsep=vsep,
                              padtop=padtop, padbottom=padbottom, units=units)
    assert 'not tall enough' in str(excinfo.value)
