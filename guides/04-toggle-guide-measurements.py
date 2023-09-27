# menuTitle : Toggle guide measurements
# shortCut  : command+shift+g

"""
    Toggle visibility of guideline measurement labels
"""

from mojo.UI import getDefault, setDefault, preferencesChanged

if getDefault("defaultGuidelineShowMeasurment") == 0:
    setDefault("defaultGuidelineShowMeasurment", 1)
else:
    setDefault("defaultGuidelineShowMeasurment", 0)

preferencesChanged()