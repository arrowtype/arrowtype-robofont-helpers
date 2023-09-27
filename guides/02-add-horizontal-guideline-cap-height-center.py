# menuTitle : Add horizontal guide to cap-height center

"""
    Add horizontal guide in the middle of the current glyphs’s cap-height
"""

f = CurrentFont()
g = CurrentGlyph()

capCenter = f.info.capHeight / 2

g.appendGuideline((0,capCenter), 0,  name="capCenter")
