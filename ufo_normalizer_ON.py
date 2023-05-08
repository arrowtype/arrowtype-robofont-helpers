"""
    A very simple script to turn on UFO Normalization. From the UFO Normalizer GitHub repo.

    https://github.com/unified-font-object/ufoNormalizer
"""

from mojo.UI import setDefault, getDefault

setDefault("shouldNormalizeOnSave", True)

print("shouldNormalizeOnSave is set to " + str(getDefault("shouldNormalizeOnSave")))