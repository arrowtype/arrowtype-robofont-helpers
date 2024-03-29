# copy and decompose glyphs with new names

# TODO: move *ALL* layers of the glyph move. Currently, this only moves the glyph in the foreground/default layer.

# import AskString from robofont's mojo UI library
from mojo.UI import AskString

# get the current font
f = CurrentFont()

# set duplicated glyphs to skip export?
skipExport = False

# get currently selected glyphs as a list
glyphsToCopy = f.selectedGlyphNames

# ask user for a suffix to add to duplicated glyphs
newGlyphSuffix = AskString(
    'Enter a new suffix for duplicate glyphs, e.g. "alt1"')

# if the user cancels or inputs an empty string, cancel the script
if newGlyphSuffix == "":
    print("canceled")


# if the script is valid, keep going
else:

    # loop through list of selected glyphs
    for glyph in glyphsToCopy:
        # get the base name of the glyph (before the period)
        baseNameOfGlyph = glyph.split('.')[0]

        # form the new glyph name
        newGlyphName = baseNameOfGlyph + "." + newGlyphSuffix

        # if the new glyph name already exists, don't overwrite it with the new one
        if newGlyphName in f.glyphOrder:
            print("sorry," + newGlyphName + " already exists.")

        # if the new glyph name doesn't already exist..
        if newGlyphName not in f.glyphOrder:

            # duplicate the selected glyph with the new glyph name
            f.insertGlyph(f[glyph], newGlyphName)

            # delete unicode value from new glyph (if you don't, it causes issues elsewhere)
            f[newGlyphName].unicode = None
            
            if skipExport:
                # set new glyph to be non-exporting            
                try:
                    f.lib["public.skipExportGlyphs"].append(newGlyphName)
                except KeyError:
                    print("No skipExportGlyphs lib yet.")
                    f.lib["public.skipExportGlyphs"] = []
                    f.lib["public.skipExportGlyphs"].append(newGlyphName)

            # let the user know it was made
            print(newGlyphName + " is created!")
