import math

from numpy import *

import wx

from CustomEvents import EVT_POLYGON_NEW
from CustomEvents import EVT_POLYGON_CLEAR
from CustomEvents import EVT_POLYGON_CLEAR_ALL
from CustomEvents import EVT_POLYGON_NEXT
from CustomEvents import EVT_POLYGON_PREV
from CustomEvents import EVT_POLYGON_RESET
from CustomEvents import EVT_RASTER_RESIZE
from CustomEvents import EVT_HELP_LINES
from CustomEvents import EVT_TOGGLE_POLYGON_TYPE

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
        self.Bind(EVT_HELP_LINES, self.onHelpLine)
        self.Bind(EVT_TOGGLE_POLYGON_TYPE, self.onTogglePolygonType)
        
        self.rasterSize = 5
        self.rasterPosition = 0, 0
        self.prevRasterPosition = 0, 0
        self.screenPosition = 0, 0
        self.polygon = []
        self.polygonVault = []
        self.polygonVault.append([])
        self.polygonTypeMap = {0:0}
        self.polygonIndex = 0
        
        self.helpLines = []
        
        self.parent = parent
        
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
    def setGraphSize(self, size):
        self.rasterSize = size
        
    def onPolygonNew(self, event):
        self.polygonVault.append([])
        self.polygonIndex = len(self.polygonVault)-1
        self.polygonTypeMap[self.polygonIndex] = 0
        self.updateDrawing()
    
    def onPolygonClear(self, event):
        self.polygonVault[self.polygonIndex] = []
        self.updateDrawing()

    def onPolygonClearAll(self, event):
        self.polygonVault = []
        self.polygonVault.append([])
        self.polygonTypeMap = {0 : 0}
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
    
    def onHelpLine(self, event):
        polygon  = self.polygonVault.pop(self.polygonIndex)
        self.polygonVault.append([])
        self.helpLines.append(polygon)
        self.updateDrawing()
    
    def onTogglePolygonType(self, event):
        if 0 == self.polygonTypeMap[self.polygonIndex]:
            self.polygonTypeMap[self.polygonIndex] = 1
        else:
            self.polygonTypeMap[self.polygonIndex] = 0
        self.updateDrawing()
        
    def onRasterResize(self, event):
        self.rasterSize = event.attr1
        self.updateDrawing()
                
    def onLButtonUp(self, event):
        self.polygonVault[self.polygonIndex].append(self.rasterPosition)
        self.prevRasterPosition = self.rasterPosition

        pointAddEvent = PointAddEvent(attr1=self.rasterPosition[0], attr2=self.rasterPosition[1])
        wx.PostEvent(self.parent, pointAddEvent)
        self.updateDrawing()
        
    def onMouseMove(self, event):
        x, y = event.GetPosition()
        
        newPosition = self.screenToRasterPosition([x, y])
        
        if newPosition != self.rasterPosition:
            self.rasterPosition = newPosition
            rasterPositionEvent = RasterPositionEvent(attr1=newPosition, attr2=self.prevRasterPosition)
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
        self.drawHelpLines(dc)
        
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
                if 0 == self.polygonTypeMap[count]:
                    self.drawPolygon(dc, polygon, False)
                else:
                    self.drawHatch(dc, polygon)
            count += 1
        
        #draw active polygon
        if -1 != self.polygonIndex:
            polygon = self.polygonVault[self.polygonIndex]
            dc.SetPen(wx.Pen(wx.RED))
            if 0 == self.polygonTypeMap[self.polygonIndex]:
                self.drawPolygon(dc, polygon, True)
            else:
                self.drawHatch(dc, polygon)
            
    def drawPolygon(self, dc, polygon, drawPoints):        
        if len(polygon) > 1:
            px, py = self.rasterToScreenPosition(polygon[0])
            
            for point in polygon[1:]:
                cx, cy = self.rasterToScreenPosition(point)
                dc.DrawLine(px, py, cx, cy)
                px, py = cx, cy
            
        if drawPoints:
            for point in polygon:
                index = polygon.index(point)
                if len(polygon)-1 > index:
                    self.drawDirectionArrow(dc, point, polygon[index+1])
                else:
                    cx, cy = self.rasterToScreenPosition(point)
                    dc.DrawCircle(cx, cy, 3)
    
    def drawHatch(self, dc, polygon):
        if len(polygon) > 1:
            for i in xrange(0, len(polygon)-1, 2):
                x1, y1 = self.rasterToScreenPosition(polygon[i])
                x2, y2 = self.rasterToScreenPosition(polygon[i+1])
                dc.DrawLine(x1, y1, x2, y2)
                
                
    def drawDirectionArrow(self, dc, curr, next):
        angle = 2.8
        rotMatrix = array([[cos(angle), -sin(angle)], 
                           [sin(angle), cos(angle)]])
                          
        rotMatrix2 = array([[cos(-angle), -sin(-angle)], 
                            [sin(-angle), cos(-angle)]])

        currPoint = array([float(curr[0]), float(curr[1])])
        nextPoint = array([float(next[0]), float(next[1])])
        
        vec = (nextPoint-currPoint)
        vec = vec / linalg.norm(vec) * (float(self.rasterSize)/15.)
        endPoint = currPoint + vec
        
        arrow1 = rotMatrix.dot(vec)
        arrow2 = rotMatrix2.dot(vec)
        
        arrow1 = arrow1 + endPoint
        arrow2 = arrow2 + endPoint
        
        x, y = self.rasterToScreenPosition([endPoint[0], endPoint[1]])
        x2, y2 = self.rasterToScreenPosition([arrow1[0], arrow1[1]])
        x3, y3 = self.rasterToScreenPosition([arrow2[0], arrow2[1]])
        
        dc.DrawLine(x, y, x2, y2)
        dc.DrawLine(x, y, x3, y3)
        
    def drawHelpLines(self, dc):
        pen = wx.Pen(wx.CYAN)
        #wx.SetColor(wx.GREEN)
        pen.SetStyle(wx.STIPPLE)
        dc.SetPen(pen)
        
        for helpLine in self.helpLines:
            self.drawPolygon(dc, helpLine, False)
        
    def refreshPolygon(self):
        self.Update()
        self.Refresh()
        polygonRefreshEvent = PolygonRefreshEvent(attr1=self.polygonVault[self.polygonIndex], attr2=self.polygonTypeMap[self.polygonIndex])
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