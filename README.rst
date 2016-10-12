panel-plots
===========

A simple to use and understand system for making panel plots with matplotlib.
The panel-plots package is designed to make it easy to create panel plots with
specific sizes, either panel size or overall figure size, maing it particularly
suitable for generating figures for journal articles where you need to prepare
an image of a particular size and ensure consistent and correct font sizing.


Getting started
---------------

The panel-plots package only manages location information, it leaves everything
else up to you (and matplotlib). A simple example is to create a 2x3 panel plot
of a specified total width. Rremember, knowing the width of the plot allows you
to select the same font size as in your document and know the fonts will work
out being the same size::

    import matplotlib.pyplot as plt
    from panels import FigureSizeLocator

    loc = FigureSizeLocator(2, 3, figwidth=150, hsep=12, vsep=12,
                            padleft=10, padright=10, padtop=10, padbottom=10)
    fig = plt.figure(figsize=loc.figsize)
    
    for i, pos in enumerate(loc.panel_position_iterator()):
        ax = fig.add_axes(pos)
        ax.plot([0, 1, 2], [3, 2, 1])
        ax.set_title('Panel #{}'.format(i))

    plt.show()

You can do a similar thing but specify the size of the individual panels using
the `PanelSizeLocator` locator.
