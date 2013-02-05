import wx
from MainFrame import MainFrame

app = wx.App(False)
wx.InitAllImageHandlers()
frame = MainFrame()
frame.Show(True)
app.MainLoop()