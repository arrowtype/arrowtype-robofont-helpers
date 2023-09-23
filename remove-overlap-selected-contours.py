# menutitle: Remove Overlap in Selected Contours
# shortcut: control+command+o


g = CurrentGlyph()

g.prepareUndo("remove overlap")

# Count number of 
contours = len(g.contours)

selectedContours = 0


for c in g:
    if c.selected:
        c.removeOverlap()
        
        selectedContours += 1
        

#if all contours or no contours selected, remove overlap for full glyph
if selectedContours == contours or selectedContours == 0:
    g.removeOverlap()
        

g.performUndo()