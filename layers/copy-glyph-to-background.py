# menutitle: Copy current glyph foreground to background
# shortcut: control+command+b

font = CurrentFont()
glyph = CurrentGlyph()

bgLayerName = font.layers[1].name

glyph.getLayer(bgLayerName).clear()

glyph.layers[0].copyLayerToLayer("foreground", bgLayerName)

# apparently, better than matching `width`
glyph.getLayer(bgLayerName).leftMargin = glyph.getLayer("foreground").leftMargin
glyph.getLayer(bgLayerName).rightMargin = glyph.getLayer("foreground").rightMargin