"""
    Open UFOs in simple font windows, which makes it faster to work on many UFOs at one time.

    Script from the RoboFont Docs.

    This is the latest version available from
    https://robofont.com/documentation/tutorials/working-with-large-fonts/
"""

from AppKit import NSURL, NSDocumentController
from vanilla import Window, List
from mojo.subscriber import Subscriber, WindowController
from lib.doodleDocument import DoodleDocument
from mojo.UI import OpenGlyphWindow, OpenSpaceCenter, OpenFontInfoSheet
from mojo.roboFont import OpenFont


class SimpleFontWindow(Subscriber, WindowController):

    def __init__(self, font):
        self._font = font
        self._canUpdateChangeCount = True
        super().__init__()

    def build(self):
        self.w = Window((250, 500), "SimpleFontWindow", minSize=(200, 300))
        glyphs = sorted(font.keys())

        self.w.glyphs = List((0, 0, -0, -0),
                             glyphs,
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
        self.w.addToolbar(toolbarIdentifier="SimpleToolbar", toolbarItems=toolbarItems)

        windowController = self.w.getNSWindowController()
        windowController.setShouldCloseDocument_(True)

        try:   # RF >= 3.3
            self._font.shallowDocument().addWindowController_(windowController)
        except AttributeError:
            if not font.path:
                return

            document = DoodleDocument.alloc().init()
            document.setFileURL_(NSURL.fileURLWithPath_(font.path))

            dc = NSDocumentController.sharedDocumentController()
            dc.addDocument_(document)

            self._font.UIdocument().addWindowController_(windowController)

        self._font.addObserver(self, "fontChanged", "Font.Changed")

    def started(self):
        self.w.open()

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

    def fontDidChange(self, info):
        if self._canUpdateChangeCount:
            try:   # RF >= 3.3
                self._font.shallowDocument().updateChangeCount_(0)
            except Exception:
                self._font.UIdocument().updateChangeCount_(0)


if __name__ == '__main__':
    fonts = OpenFont(showInterface=False)
    if not isinstance(fonts, list):
        fonts = [fonts]

    for font in fonts:
        SimpleFontWindow(font)