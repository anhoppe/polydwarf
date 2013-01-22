import wx

from CustomEvents import EVT_POLYGON_NEW
from CustomEvents import EVT_POLYGON_CLEAR
from CustomEvents import EVT_POLYGON_CLEAR_ALL
from CustomEvents import EVT_POLYGON_NEXT
from CustomEvents import EVT_POLYGON_PREV
from CustomEvents import EVT_POLYGON_RESET
from CustomEvents import EVT_RASTER_RESIZE

from CustomEvents import PointAddEvent
from CustomEvents import PolygonRefreshEvent
from CustomEvents import RasterPositionEvent

AXIS_HELP_LINE_LEN = 3

class PolyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOTION, self.onMouseMove)
        self.Bind(wx.EVT_LEFT_UP, self.onLButtonUp)
        
        self.Bind(EVT_POLYGON_NEW, self.onPolygonNew)
        self.Bind(EVT_POLYGON_CLEAR, self.onPolygonClear)
        self.Bind(EVT_POLYGON_CLEAR_ALL, self.onPolygonClearAll)
        self.Bind(EVT_POLYGON_NEXT, self.onPolygonNext)
        self.Bind(EVT_POLYGON_PREV, self.onPolygonPrev)
        self.Bind(EVT_POLYGON_RESET, self.onPolygonReset)
        self.Bind(EVT_RASTER_RESIZE, self.onRasterResize)
        
        
        self.rasterSize = 5
        self.rasterPosition = 0, 0
        self.screenPosition = 0, 0
        self.polygon = []
        self.polygonVault = []
        self.polygonVault.append([])
        self.polygonIndex = 0
        self.parent = parent
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
    def setGraphSize(self, size):
        self.rasterSize = size
        
    def onPolygonNew(self, event):
        self.polygonVault.append([])
        self.polygonIndex = len(self.polygonVault)-1
        self.updateDrawing()
    
    def onPolygonClear(self, event):
        self.polygonVault[self.polygonIndex] = []
        self.updateDrawing()

    def onPolygonClearAll(self, event):
        self.polygonVault = []
        self.polygonVault.append([])
        self.polygonIndex = 0
        self.updateDrawing()
    
    def onPolygonNext(self, event):
        if self.polygonIndex < len(self.polygonVault)-1:
            self.polygonIndex += 1
            self.refreshPolygon()
            self.updateDrawing()
    
    def onPolygonPrev(self, event):
        if self.polygonIndex > 0:
            self.polygonIndex -= 1
            self.refreshPolygon()
            self.updateDrawing()
            
    def onPolygonReset(self, event):
        self.polygonVault[self.polygonIndex] = event.attr1
        self.updateDrawing()
        
    def onRasterResize(self, event):
        self.rasterSize = event.attr1
        self.updateDrawing()
                
    def onLButtonUp(self, event):
        self.polygonVault[self.polygonIndex].append(self.rasterPosition)

        pointAddEvent = PointAddEvent(attr1=self.rasterPosition[0], attr2=self.rasterPosition[1])
        wx.PostEvent(self.parent, pointAddEvent)
        self.updateDrawing()
        
    def onMouseMove(self, event):
        x, y = event.GetPosition()
        
        newPosition = self.screenToRasterPosition([x, y])
        
        if newPosition != self.rasterPosition:
            self.rasterPosition = newPosition
            rasterPositionEvent = RasterPositionEvent(attr1=newPosition)
            wx.PostEvent(self.parent, rasterPositionEvent)
            self.updateDrawing()
            
    def onSize(self, event):
        size = self.ClientSize
        self._buffer = wx.EmptyBitmap(*size)
        self.updateDrawing()
            
    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self, self._buffer)

    def updateDrawing(self):
        dc = wx.MemoryDC()
        dc.SelectObject(self._buffer)
        
        dc.SetBackground( wx.Brush("White") )
        dc.Clear() # make sure you clear the bitmap!
        self.drawRaster(dc)
        self.drawMouseRasterPoint(dc)
        self.drawPolygons(dc)    
        
        del dc # need to get rid of the MemoryDC before Update() is called.
        self.Update()        
        self.Refresh(eraseBackground=False)

    def drawRaster(self, dc):
        w, h = self.GetSize()
        
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush(wx.WHITE))
        
        wHalf = w/2 
        hHalf = h/2
        # draw the axes
        dc.DrawLine(0, hHalf, w, hHalf)
        dc.DrawLine(wHalf, 0, wHalf, h)
        
        ##draw the axis help lines
        for i in range(1, self.rasterSize):
            xRasterDist = i*wHalf / self.rasterSize
            yRasterDist = i*hHalf / self.rasterSize
            dc.DrawLine(wHalf + xRasterDist, hHalf,
                        wHalf + xRasterDist, hHalf + AXIS_HELP_LINE_LEN)
            dc.DrawLine(wHalf - xRasterDist, hHalf,
                        wHalf - xRasterDist, hHalf - AXIS_HELP_LINE_LEN)
            
            dc.DrawLine(wHalf, hHalf + yRasterDist,
                        wHalf+AXIS_HELP_LINE_LEN, hHalf + yRasterDist)
            dc.DrawLine(wHalf, hHalf - yRasterDist,
                        wHalf-AXIS_HELP_LINE_LEN, hHalf - yRasterDist)
            
    def drawMouseRasterPoint(self, dc):
        brush = wx.Brush(wx.RED)
        pen = wx.Pen(wx.RED)

        dc.SetPen(pen)
        dc.SetBrush(brush)
            
        x ,y = self.rasterToScreenPosition(self.rasterPosition)
        dc.DrawCircle(x, y, 5)

    def drawPolygons(self, dc):
        # Draw inactive polygons
        count = 0
        dc.SetPen(wx.Pen(wx.LIGHT_GREY))
        
        for polygon in self.polygonVault:
            if count <> self.polygonIndex:
                self.drawPolygon(dc, polygon, False)
            count += 1
        
        #draw active polygon
        dc.SetPen(wx.Pen(wx.RED))
        self.drawPolygon(dc, self.polygonVault[self.polygonIndex], True)
            
    def drawPolygon(self, dc, polygon, drawPoints):
        
        if len(polygon) > 1:
            px, py = self.rasterToScreenPosition(polygon[0])
            
            for point in polygon[1:]:
                cx, cy = self.rasterToScreenPosition(point)
                dc.DrawLine(px, py, cx, cy)
                px, py = cx, cy
            
        if drawPoints:
            for point in polygon:
                cx, cy = self.rasterToScreenPosition(point)
                dc.DrawCircle(cx, cy, 3)
                

    def refreshPolygon(self):
        self.Update()
        self.Refresh()
        polygonRefreshEvent = PolygonRefreshEvent(attr1=self.polygonVault[self.polygonIndex])
        wx.PostEvent(self.parent, polygonRefreshEvent)
        
    def screenToRasterPosition(self, screenPosition):
        x, y = screenPosition
        w, h = self.GetSize()
        rs = self.rasterSize*2

        rasterPosition = x * rs / w - self.rasterSize, self.rasterSize - y * rs / h
        
        return rasterPosition
        
    def rasterToScreenPosition(self, rasterPosition):
        x, y = rasterPosition
        w, h = self.GetSize()
        rs = self.rasterSize*2
        
        screenPosition = (self.rasterSize + x) * w/rs, (self.rasterSize - y) * h/rs 
        
        return screenPosition