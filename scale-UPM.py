"""
    Used to scale a UFO’s UPM, and everything in the UFO.

    From @gferreira in the RoboFont Forum:
    https://forum.robofont.com/topic/717/existing-script-to-scale-upm-plus-dimensions-glyphs-components-kerning-etc/3
"""

font = CurrentFont()

print(font)

newUpm = 2048
oldUpm = font.info.unitsPerEm
factor = newUpm / oldUpm

for layer in font.layers:

    for glyph in layer:

        for contour in glyph:
            contour.scaleBy(factor)

        for anchor in glyph.anchors:
            anchor.scaleBy(factor)

        for guideline in glyph.guidelines:
            guideline.scaleBy(factor)

        glyph.width *= factor

font.kerning.scaleBy(factor)

for guideline in font.guidelines:
    guideline.scaleBy(factor)

for attr in ['unitsPerEm', 'descender', 'xHeight', 'capHeight', 'ascender']:
    oldValue = getattr(font.info, attr)
    newValue = oldValue * factor
    setattr(font.info, attr, newValue)

font.changed()