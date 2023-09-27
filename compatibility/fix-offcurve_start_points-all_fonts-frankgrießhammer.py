"""
    Goes through all open fonts and changes offcurve start points to oncurve start points,
    which is necessary for predictable interpolation/compatibility.

    From https://github.com/roboDocs/ScaleFast/issues/5, made to run through all open fonts.

    Script by Frank Grießhammer. Used/shared with permission.
"""

from fontTools.ufoLib.pointPen import PointToSegmentPen


def redraw_glyph(g):
    contours = []

    for contour in g.contours:
        points = [p for p in contour.points]
        while points[0].type == 'offcurve':
            points.append(points.pop(0))
        contours.append(points)

    g.prepareUndo('redraw')
    rg = RGlyph()
    ppen = PointToSegmentPen(rg.getPen())

    for contour in contours:
        ppen.beginPath()
        for point in contour:
            if point.type == 'offcurve':
                ptype = None
            else:
                ptype = point.type
            ppen.addPoint((point.x, point.y), ptype)
        ppen.endPath()

    g.clearContours()
    g.appendGlyph(rg)
    g.performUndo()

for f in AllFonts():

    glyphs_with_contours = [g for g in f if len(g.contours)]
    glyphs_with_offcurve_start = []

    for g in glyphs_with_contours:
        for contour in g.contours:
            first_point = contour.points[0]
            first_bPoint = contour.bPoints[0]
            first_point_coords = (first_point.x, first_point.y)
            if first_point_coords != first_bPoint.anchor:
                glyphs_with_offcurve_start.append(g)

    for g in glyphs_with_offcurve_start:
        print(g.name)
        redraw_glyph(g)
