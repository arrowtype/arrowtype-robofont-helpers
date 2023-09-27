# menuTitle : Add vertical guide to glyph center

"""
    Add vertical guide in the middle of the current Glyph’s width
"""

f = CurrentFont()
g = CurrentGlyph()

if f.info.italicAngle:
    italicAngle = f.info.italicAngle
else:
    italicAngle = 0

glyphCenter = g.width / 2

print(glyphCenter)

# account for italic angle
italicOffset = f.lib["com.typemytype.robofont.italicSlantOffset"]
if italicOffset:
    xPos = italicOffset
else:
    xPos = 0

# add the guideline
g.appendGuideline((glyphCenter + xPos, 0), 90+italicAngle)
