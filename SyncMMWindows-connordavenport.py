"""
    Script by Connor Davenport.
    
    https://gist.github.com/connordavenport/17717ed4187a31b572eafa0e77e9cb09
"""

import metricsMachine
from mm4.mmScripting import MetricsMachineScriptingError
from vanilla import FloatingWindow, List, CheckBox, PopUpButton
from mojo.events import addObserver, removeObserver
from AppKit import *
from mojo.UI import Message

class SyncMM:

	def __init__(self):

		self.altDown = None
		
		self.fontList = []
		self.scaledWindows = []
		self.pointSizes = ["Auto", "50", "75", "100", "125", "150", "200", "250", "300", "350", "400", "450", "500"]

		self.w = FloatingWindow((200, 240), "Sync MM Windows")
		self.w.nameList = List((10,10,-10,-60), [])
		self.updateList(None)

		self.w.t = CheckBox((10,-50,100,20),"Tile Windows", callback=self.tileCallback)
		self.w.c = CheckBox((10,-30,100,20),"Sync Sizes")

		self.w.p = PopUpButton((-80,-30,70,20), self.pointSizes, callback=self.setAllPointSizes)

		addObserver(self, "pairChanged", "MetricsMachine.currentPairChanged")
		addObserver(self, "updateList", "fontDidClose")
		addObserver(self, "updateList", "fontWillOpen")

		self.w.bind("close", self.removeObs)
		self.w.open()

	def updateList(self, info):
		self.fontList = [f"{f.info.familyName} {f.info.styleName}" for f in AllFonts()]
		self.w.nameList.set(self.fontList)

	def removeObs(self, sender):
		removeObserver(self, "MetricsMachine.currentPairChanged")
		removeObserver(self, "fontWillClose")
		removeObserver(self, "fontWillOpen")


	# ================================
	'''
	Window code taken from Tal Leming's Metrics Machine
	'''

	def _getMainWindowControllerForFont(self, font=None):
		if font is None:
			font = CurrentFont()
		for other in AllFonts():
			if other != font:
				continue
			document = other.document()
			for controller in document.windowControllers():
				window = controller.window()
				if hasattr(window, "windowName") and window.windowName() == "MetricsMachineMainWindow":
					delegate = window.delegate()
					mmController = delegate.vanillaWrapper()
					return mmController
		raise MetricsMachineScriptingError("A MetricsMachine window is not open for %r." % font)

	def SetListSelection(self, pair=None, font=None):
		window = self._getMainWindowControllerForFont(font)
		pairList = window.pairList
		pairList.setSelection(pair)

	def getWindowPosSize(self, font=None):
		window = self._getMainWindowControllerForFont(font)
		x,y,w,h = window.w.getPosSize()
		
		return x,y,w,h

	def setWindowPosSize(self, posSize, font=None):
		window = self._getMainWindowControllerForFont(font)
		window.w.setPosSize(posSize)

	def getPointSize(self, font=None):
		window = self._getMainWindowControllerForFont(font)
		return window.editView.pairView.getPointSize()

	def setPointSize(self, pointSize, font=None):
		window = self._getMainWindowControllerForFont(font)
		window.editView.pairView.setPointSize(pointSize)

	def setAllPointSizes(self,sender):
		'''You cant set a window's EditView text to a random PointSize, instead
		we can just use MM's set of predefined values'''

		fonts = metricsMachine.AllFonts()
		fontSelection = [self.fontList[i] for i in self.w.nameList.getSelection()]
		if sender.get() == 0:
			pSize = None
		else:
			pSize = int(self.pointSizes[sender.get()])

		for fs in fonts:
			try:
				if f"{fs.info.familyName} {fs.info.styleName}" in fontSelection:
					self.setPointSize(pSize,fs)
			except MetricsMachineScriptingError:
				pass

	# ================================
		
	'''
	tiling code taken from Frederik Berlean's Arrange Windows
	'''

	def getWindowSize(self,window):
		w,h = (window.frame().size)
		x,y = (window.frame().origin)
		return (x,y,w,h)

	def tileCallback(self, sender):
		if sender.get() == 1:

			self.w.c.set(0)
			self.w.c.enable(False)

			windows = [w for w in NSApp().orderedWindows() if w.isVisible()]

			screen = NSScreen.mainScreen()
			(x, y), (w, h) = screen.visibleFrame()

			self.altDown = NSEvent.modifierFlags() & NSAlternateKeyMask

			NSApp().arrangeInFront_(None)

			windowsToHide = []
			windowsToTile = []
			for window in windows:
				if hasattr(window, "windowName") and window.windowName() == "MetricsMachineMainWindow":
					windowsToTile.append(window)

			tileInfo = {
						1 : [[1]],
						2 : [[1],[1]],
						3 : [[],[1, 1, 1]],
						4 : [[1, 1], [1, 1]],
						5 : [[1, 1], [1, 1, 1]],
						}

			if windowsToTile:
				if len(windowsToTile) > list(tileInfo.keys())[-1]:
					Message("Limit is 10 MM Windows")

				arrangement = tileInfo[len(windowsToTile)]					
				maxHeight = len(arrangement)
				diffx = x
				diffy = y
				c = 0
				for i in arrangement:
					maxWidth = len(i)		
					for j in i:
						window = windowsToTile[c]
						self.scaledWindows.append((window,self.getWindowSize(window)))
						window.setFrame_display_animate_(NSMakeRect(diffx, diffy, w/float(maxWidth), h/float(maxHeight)), True, self.altDown)
						c += 1

						diffx += w/float(maxWidth)
					diffx = x
					diffy += h/float(maxHeight)
		else:
			self.w.c.enable(True)
			for win, posSize in self.scaledWindows:
				xs,ys,ws,hs = posSize
				win.setFrame_display_animate_(NSMakeRect(xs,ys,ws,hs), True, self.altDown)

		
	def pairChanged(self, sender):
		cp = sender["pair"]

		pl = metricsMachine.GetPairList()
		pos = self.getWindowPosSize(CurrentFont())
		pvt = metricsMachine.GetPreviewText(CurrentFont())
		# ptsz = self.getPointSize(CurrentFont())

		fonts = metricsMachine.AllFonts()
		fontSelection = [self.fontList[i] for i in self.w.nameList.getSelection()]

		for fs in fonts:
			try:
				if f"{fs.info.familyName} {fs.info.styleName}" in fontSelection:
					if self.w.c.get() == 1:
						x,y,w,h = self.getWindowPosSize(fs)

						if (pos[2],pos[3]) != (w,h):
							self.setWindowPosSize((x,y,pos[2],pos[3]),fs)
					if metricsMachine.GetPreviewText(fs) != pvt:
						metricsMachine.SetPreviewText(pvt, fs)
					if metricsMachine.GetPairList(fs) != pl:
						metricsMachine.SetPairList(pl, fs)
					while metricsMachine.GetCurrentPair(fs) != cp:
						if fs != metricsMachine.CurrentFont():
							metricsMachine.SetCurrentPair(cp,fs)
							self.SetListSelection(cp,fs)

			except MetricsMachineScriptingError:
				pass


SyncMM()