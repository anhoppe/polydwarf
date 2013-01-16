import wx
from PolyPanel import PolyPanel
from ControlPanel import ControlPanel

from CustomEvents import EVT_POINT_ADD
from CustomEvents import EVT_POLYGON_NEW
from CustomEvents import EVT_POLYGON_CLEAR
from CustomEvents import EVT_POLYGON_CLEAR_ALL
from CustomEvents import EVT_POLYGON_NEXT
from CustomEvents import EVT_POLYGON_PREV
from CustomEvents import EVT_POLYGON_REFRESH
from CustomEvents import EVT_POLYGON_RESET
from CustomEvents import EVT_RASTER_RESIZE
from CustomEvents import EVT_RASTER_POSITION

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "PolyDwarf")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # add the control panel
        self.controlPanel = ControlPanel(self)
        sizer.Add(self.controlPanel, 0, wx.EXPAND)
        
        # add the polygon draw panel
        self.polyPanel = PolyPanel(self)
        sizer.Add(self.polyPanel, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.Bind(EVT_POINT_ADD, self.onControlPanelEvent)
        self.Bind(EVT_POLYGON_REFRESH, self.onControlPanelEvent)
        self.Bind(EVT_RASTER_POSITION, self.onControlPanelEvent)
        
        self.Bind(EVT_POLYGON_NEW, self.onPolyPanelEvent)
        self.Bind(EVT_POLYGON_CLEAR, self.onPolyPanelEvent)
        self.Bind(EVT_POLYGON_CLEAR_ALL, self.onPolyPanelEvent)		
        self.Bind(EVT_POLYGON_NEXT, self.onPolyPanelEvent)
        self.Bind(EVT_POLYGON_PREV, self.onPolyPanelEvent)
        self.Bind(EVT_POLYGON_RESET, self.onPolyPanelEvent)
        self.Bind(EVT_RASTER_RESIZE, self.onPolyPanelEvent)
 
    def onControlPanelEvent(self, event):
        self.Update()
        self.Refresh()
        self.controlPanel.ProcessEvent(event)
        
    def onPolyPanelEvent(self, event):
        self.polyPanel.ProcessEvent(event)
    