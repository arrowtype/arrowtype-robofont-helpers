"""
But actually, you can assign a shortcut to the basic right-click function under RoboFont Preferences > Glyph View > Hot Keys.
"""


# menutitle: Remove Overlap in Selected Contours

g = CurrentGlyph()

with g.undo("Remove overlap"):
    d_glyph = g.asDefcon()
    sel = d_glyph.selection
    sel.removeOverlap()