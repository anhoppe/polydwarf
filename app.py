import wx
from MainFrame import MainFrame

app = wx.App(False)
frame = MainFrame()
frame.Show(True)
app.MainLoop()