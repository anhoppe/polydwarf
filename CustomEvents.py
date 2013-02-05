import wx.lib.newevent

PointAddEvent, EVT_POINT_ADD = wx.lib.newevent.NewEvent()

PolygonNewEvent, EVT_POLYGON_NEW = wx.lib.newevent.NewEvent()
PolygonClearEvent, EVT_POLYGON_CLEAR = wx.lib.newevent.NewEvent()
PolygonClearAllEvent, EVT_POLYGON_CLEAR_ALL = wx.lib.newevent.NewEvent()
PolygonNextEvent, EVT_POLYGON_NEXT = wx.lib.newevent.NewEvent()
PolygonPrevEvent, EVT_POLYGON_PREV = wx.lib.newevent.NewEvent()
PolygonRefreshEvent, EVT_POLYGON_REFRESH = wx.lib.newevent.NewEvent()
PolygonResetEvent, EVT_POLYGON_RESET = wx.lib.newevent.NewEvent()
RasterResizeEvent, EVT_RASTER_RESIZE = wx.lib.newevent.NewEvent()
RasterPositionEvent, EVT_RASTER_POSITION = wx.lib.newevent.NewEvent()
HelpLineEvent, EVT_HELP_LINES = wx.lib.newevent.NewEvent()