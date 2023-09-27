"""
    Script from the RoboFont Docs.

    There is a newer version which may or may not work better:
    https://robofont.com/documentation/tutorials/working-with-large-fonts/
"""

from AppKit import NSURL, NSDocumentController
from vanilla import Window, List
from defconAppKit.windows.baseWindow import BaseWindowController
from lib.doodleDocument import DoodleDocument
from mojo.UI import OpenGlyphWindow, OpenSpaceCenter, OpenFontInfoSheet


class SimpleFontWindow(BaseWindowController):

    def __init__(self, font):

        self._font = font

        if font.path:
            document = DoodleDocument.alloc().init()
            document.setFileURL_(NSURL.fileURLWithPath_(font.path))

            dc = NSDocumentController.sharedDocumentController()
            dc.addDocument_(document)

        self._canUpdateChangeCount = True

        self.w = Window((250, 500), "SimpleFontWindow", minSize=(200, 300))

        glyphs = sorted(font.keys())

        self.w.glyphs = List((0, 0, -0, -0), glyphs,
                             doubleClickCallback=self.openGlyph)

        toolbarItems = [
            dict(itemIdentifier="spaceCenter",
                 label="Space Center",
                 imageNamed="toolbarSpaceCenterAlternate",
                 callback=self.openSpaceCenter
                 ),
            dict(itemIdentifier="fontInfo",
                 label="Font Info",
                 imageNamed="toolbarFontInfo",
                 callback=self.openFontInfo
                 )
        ]
        self.w.addToolbar(toolbarIdentifier="SimpleToolbar",
                          toolbarItems=toolbarItems)

        windowController = self.w.getNSWindowController()
        windowController.setShouldCloseDocument_(True)
        self._font.UIdocument().addWindowController_(windowController)

        self._font.addObserver(self, "fontChanged", "Font.Changed")

        self.setUpBaseWindowBehavior()
        self.w.open()

        # self.openFirstGlyph()

    def openGlyph(self, sender):
        sel = sender.getSelection()
        if sel:
            i = sel[0]
            name = sender[i]
            self._canUpdateChangeCount = False
            OpenGlyphWindow(self._font[name])
            self._canUpdateChangeCount = True

    def openSpaceCenter(self, sender):
        self._canUpdateChangeCount = False
        OpenSpaceCenter(self._font)
        self._canUpdateChangeCount = True

    def openFontInfo(self, sender):
        self._canUpdateChangeCount = False
        OpenFontInfoSheet(self._font, self.w)
        self._canUpdateChangeCount = True

    # notifications
    def fontChanged(self, notification):
        if self._canUpdateChangeCount:
            self._font.UIdocument().updateChangeCount_(0)

    # to make EditThatNextMaster work as needed

    def openFirstGlyph(self):

        glyphName = "A"
        # glyphName = "ninesuperior.afrc"

        if glyphName in font.keys():
            OpenGlyphWindow(self._font[glyphName])


fonts = OpenFont(showInterface=False)
if not isinstance(fonts, list):
    fonts = [fonts]

for font in fonts:
    print(font)
    SimpleFontWindow(font)
