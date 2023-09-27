# menuTitle : Remove guidelines in current glyph

"""
    Remove all guidelines in current glyph (doesn’t affect global guidelines)
"""

g = CurrentGlyph()

for guide in g.guidelines:
    g.removeGuideline(guide)

