# menutitle: Flip current glyph foreground to background
# shortcut: control+command+shift+b

font = CurrentFont()
glyph = CurrentGlyph()

bgLayerName = font.layers[1].name

# # apparently, better than matching `width`
# glyph.getLayer(bgLayerName).leftMargin = glyph.getLayer("foreground").leftMargin
# glyph.getLayer(bgLayerName).rightMargin = glyph.getLayer("foreground").rightMargin

glyph.getLayer(bgLayerName).width = glyph.getLayer("foreground").width

glyph.flipLayers("foreground", bgLayerName)

# also copy guidelines
for guideline in glyph.getLayer(bgLayerName).guidelines:
    glyph.getLayer("foreground").appendGuideline((guideline.x,guideline.y),guideline.angle)

# and keep anchors
for anchor in glyph.getLayer(bgLayerName).anchors:
    glyph.getLayer("foreground").appendAnchor(anchor.name, (anchor.x,anchor.y))
