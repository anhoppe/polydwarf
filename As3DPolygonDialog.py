import wx

BUTTON_OK = 1000
BUTTON_CANCEL = 1001

class As3DPolygon(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, wx.ID_ANY)

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Create settings for 3D export settings
		settingsSizer = wx.FlexGridSizer(3, 4)
		settingsSizer.AddGrowableCol(1)
		settingsSizer.AddGrowableCol(3)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "X:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textX = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textX, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "Scale:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textXScale = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textXScale, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "Y:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textY = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textY, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "Scale:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textYScale = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textYScale, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "Z:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textZ = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textZ, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		settingsSizer.Add(wx.StaticText(self, wx.ID_ANY, "Scale:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.textZScale = wx.TextCtrl(self, wx.ID_ANY)
		settingsSizer.Add(self.textZScale, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		mainSizer.Add(settingsSizer, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		# Create size for ok cancel button	
		okCancelSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.buttonOk = wx.Button(self, BUTTON_OK, "Ok")
		okCancelSizer.Add(self.buttonOk, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.Bind(wx.EVT_BUTTON, self.onButtonOk, self.buttonOk)
		
		buttonCancel = wx.Button(self, BUTTON_CANCEL, "Cancel")
		okCancelSizer.Add(buttonCancel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		self.Bind(wx.EVT_BUTTON, self.onButtonCancel, buttonCancel)

		mainSizer.Add(okCancelSizer, 0, )

		self.SetSizer(mainSizer, 0)

	def onButtonOk(self, event):
		self.EndModal(wx.ID_OK)
	
	def onButtonCancel(self, event):
		self.EndModal(wx.ID_CANCEL)