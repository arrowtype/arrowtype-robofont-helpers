# menuTitle : Add global guides to font metrics

"""
    Purpose: create (or remove) global guides on vertical metric lines of a UFO

    Why? Nodes snap to guidelines, and (maybe?) give a visual indication that they're on a guideline. I want this on the baseline, x-height, etc.
"""

from mojo.UI import setDefault

f = CurrentFont()
g = CurrentGlyph()

offsetLeft = -100

try:
    offsetLeft -= f.lib["com.typemytype.robofont.italicSlantOffset"]
except:
    pass

# set up dict of metrics guidelines
metrics = {
    "Baseline": 0,
    "Cap Height": f.info.capHeight,
    "x Height": f.info.xHeight,
    "Ascender": f.info.ascender,
    "Descender": f.info.descender,

}

oldMetricsGuidelines = False
for gl in f.guidelines:
    if (gl.name, gl.y) in metrics.items():
        oldMetricsGuidelines = True
        f.removeGuideline(gl)

if oldMetricsGuidelines:
    print("Clearing old metrics guidelines")


print("Setting new metrics guidelines")
f.appendGuideline((offsetLeft, metrics["Baseline"]), 0, name="Baseline")
f.appendGuideline((offsetLeft, metrics["Cap Height"]), 0, name="Cap Height")
f.appendGuideline((offsetLeft, metrics["x Height"]), 0, name="x Height")
f.appendGuideline((offsetLeft, metrics["Ascender"]), 0, name="Ascender")
f.appendGuideline((offsetLeft, metrics["Descender"]), 0, name="Descender")

print("Locking metrics guidelines")
for guide in f.guidelines:
    guide.locked = True

# set to False if you'd rather not have locked guidelines
setDefault("glyphViewLockGuides", True)
