import math
import wx

from CustomEvents import EVT_POINT_ADD
from CustomEvents import EVT_POLYGON_REFRESH
from CustomEvents import EVT_RASTER_POSITION

from CustomEvents import PolygonNewEvent 
from CustomEvents import PolygonClearEvent
from CustomEvents import PolygonClearAllEvent
from CustomEvents import PolygonPrevEvent 
from CustomEvents import PolygonNextEvent 
from CustomEvents import PolygonResetEvent 
from CustomEvents import RasterResizeEvent
from CustomEvents import RasterPositionEvent
from CustomEvents import HelpLineEvent
from CustomEvents import TogglePolygonTypeEvent

BUTTON_NEW = 1000
BUTTON_CLEAR = 1001
BUTTON_CLEAR_ALL = 1002
SPIN_POLY_SELECTION = 1003
TEXT_POLYGON = 1004
TEXT_RASTER_SIZE = 1005
BUTTON_COPY = 1006
BUTTON_PASTE = 1007
BUTTON_HELP_LINE = 1008
BUTTON_POLYGON_TYPE = 1009


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        
        self.parent = parent
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sizeSizer = wx.BoxSizer(wx.HORIZONTAL)
        
		# Add the raster size static text + text ctrl
        sizeSizer.Add(wx.StaticText(self, wx.ID_ANY, "Raster Size:"), 0, wx.ALIGN_CENTER_VERTICAL)
        
        self.textSize = wx.TextCtrl(self, TEXT_RASTER_SIZE, "5", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        sizeSizer.Add(self.textSize, 1, wx.ALL, 5)
        self.Bind(wx.EVT_TEXT_ENTER, self.onTextRasterSize, self.textSize)
        
        sizeSizer.AddSpacer(10)
        
		# Add the number of points display
        sizeSizer.Add(wx.StaticText(self, wx.ID_ANY, "Number of points:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		
        self.textNofPoints = wx.TextCtrl(self, wx.ID_ANY, "0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        self.nofPoints = 0
        sizeSizer.Add(self.textNofPoints, 1, wx.ALL, 5)
        
        sizeSizer.AddSpacer(10)
        
        # Add the cursor raster position
        sizeSizer.Add(wx.StaticText(self, wx.ID_ANY, "Raster Pos:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		
        self.textRasterPosition = wx.TextCtrl(self, wx.ID_ANY, "0/0", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        sizeSizer.Add(self.textRasterPosition, 1, wx.ALL, 5)

        # Add the distance form cursor to previously set point
        sizeSizer.Add(wx.StaticText(self, wx.ID_ANY, "Dist to prev:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        self.textDistToPrev = wx.TextCtrl(self, wx.ID_ANY, "-/-", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        sizeSizer.Add(self.textDistToPrev, 1, wx.ALL, 5)
        
        
        
		# add the sizer top sizer with size / raster info
        sizer.Add(sizeSizer, 0)
        
        ####################################################
        outSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.comboOutType = wx.ComboBox(self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, [], wx.CB_READONLY)
        outSizer.Add(self.comboOutType, 0)
        self.comboOutType.Append("double")
        self.comboOutType.Append("float")
        self.comboOutType.Append("int")
        self.comboOutType.SetSelection(0)
        
        
        self.textOutput = wx.TextCtrl(self, TEXT_POLYGON, "", wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onTextEnterPolygon, self.textOutput)
        outSizer.Add(self.textOutput, 1)
        
        spinButton = wx.SpinButton(self, SPIN_POLY_SELECTION, wx.DefaultPosition, wx.DefaultSize, wx.SP_VERTICAL)
        outSizer.Add(spinButton, 0)
        self.Bind(wx.EVT_SPIN_UP, self.onSpinPolySelectionUp, spinButton)
        self.Bind(wx.EVT_SPIN_DOWN, self.onSpinPolySelectionDown, spinButton)
        
        commandSizer = wx.BoxSizer(wx.VERTICAL)
        newDeleteSizer = wx.BoxSizer(wx.HORIZONTAL)
        copyPasteSizer = wx.BoxSizer(wx.HORIZONTAL)
        polygonHatchSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        outSizer.Add(commandSizer)
        commandSizer.Add(newDeleteSizer)
        commandSizer.Add(copyPasteSizer)
        commandSizer.Add(polygonHatchSizer)
        
        # create control for new delete sizer (buttons for new, clear, clear all)
        self.buttonNew = wx.Button(self, BUTTON_NEW, "New")
        newDeleteSizer.Add(self.buttonNew, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonNew, self.buttonNew)
        
        self.buttonClear = wx.Button(self, BUTTON_CLEAR, "Clear")
        newDeleteSizer.Add(self.buttonClear, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonClear, self.buttonClear)
        
        self.buttonClearAll = wx.Button(self, BUTTON_CLEAR_ALL, "Clear all")
        newDeleteSizer.Add(self.buttonClearAll, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonClearAll, self.buttonClearAll)
                
        # create control for copy'n'paste sizer
        self.buttonCopy = wx.Button(self, BUTTON_COPY, "Copy")
        copyPasteSizer.Add(self.buttonCopy, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonCopy, self.buttonCopy)
        
        self.buttonPaste = wx.Button(self, BUTTON_PASTE, "Paste")
        copyPasteSizer.Add(self.buttonPaste, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonPaste, self.buttonPaste)
        
        self.buttonHelpLine = wx.Button(self, BUTTON_HELP_LINE, "Help Line")
        copyPasteSizer.Add(self.buttonHelpLine, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonHelpLine, self.buttonHelpLine)
        
        # create control for polygon/hatch controls
        self.buttonPolygonType = wx.Button(self, BUTTON_POLYGON_TYPE, "To Hatch")
        polygonHatchSizer.Add(self.buttonPolygonType, 0)
        self.Bind(wx.EVT_BUTTON, self.onButtonPolygonType, self.buttonPolygonType)
        
        sizer.Add(outSizer, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        
        self.Bind(EVT_POINT_ADD, self.onPointAdd)
        self.Bind(EVT_POLYGON_REFRESH, self.onPolygonRefresh)
        self.Bind(EVT_RASTER_POSITION, self.onRasterPosition)
        
    def onButtonNew(self, event):
        self.textOutput.Clear()
        polygonNewEvent = PolygonNewEvent()
        self.nofPoints = 0
        self.displayNofPoints()
        wx.PostEvent(self.parent, polygonNewEvent)
        
    def onButtonClear(self, event):
        self.textOutput.Clear()
        polygonClearEvent = PolygonClearEvent()
        self.nofPoints = 0
        self.displayNofPoints()
        wx.PostEvent(self.parent, polygonClearEvent)
        
    def onButtonClearAll(self, event):
        self.textOutput.Clear()
        polygonClearAllEvent = PolygonClearAllEvent()
        self.nofPoints = 0
        self.displayNofPoints()
        wx.PostEvent(self.parent, polygonClearAllEvent)
        
    def onButtonCopy(self, event):
        self.textOutput.SetSelection(-1, -1)
        self.textOutput.Copy()
        
    def onButtonPaste(self, event):
        self.textOutput.SetSelection(-1, -1)
        self.textOutput.Paste()
        self.displayPolygon()
       
    def onButtonHelpLine(self, event):
        helpLineEvent = HelpLineEvent()
        wx.PostEvent(self.parent, helpLineEvent)
    
    def onButtonPolygonType(self, event):
        togglePolygonTypeEvent = TogglePolygonTypeEvent()
        wx.PostEvent(self.parent, togglePolygonTypeEvent)
            
    def onSpinPolySelectionUp(self, event):
        polygonNextEvent = PolygonNextEvent()
        wx.PostEvent(self.parent, polygonNextEvent)
    
    def onSpinPolySelectionDown(self, event):
        polygonPrevEvent = PolygonPrevEvent()
        wx.PostEvent(self.parent, polygonPrevEvent)
    
    def onTextEnterPolygon(self, event):
        self.displayPolygon()
    
    def onPointAdd(self, event):
        text = self.textOutput.GetValue()
        
        if text != "":
            text += ", "
        
        text += self.getFormated(event.attr1) + ", " + self.getFormated(event.attr2)
        self.textOutput.SetValue(text)
        
        self.nofPoints += 1
        self.displayNofPoints()

        
    def onPolygonRefresh(self, event):
        self.textOutput.Clear()
        text = wx.EmptyString;
        size = len(event.attr1)
        count = 0
        
        for point in event.attr1:
            text += self.getFormated(point[0]) + ", " + self.getFormated(point[1])
            if count < (size-1):
                text += ", "
            count += 1
        self.textOutput.SetValue(text)
        
        self.nofPoints = len(event.attr1)
        self.displayNofPoints()
        
        # set the state of the Polygon / Hatch button
        if 0 == event.attr2:
            self.buttonPolygonType.SetLabel("To Hatch")
        else:
            self.buttonPolygonType.SetLabel("To Polygon")

    def onRasterPosition(self, event):
        # convert current raster position to string
        currentPosition = event.attr1
        text = str(currentPosition[0])
        text += "/"
        text += str(currentPosition[1])
        self.textRasterPosition.SetValue(text)

        # calculate distance to previous position
        prevPosition = event.attr2
        dist = math.sqrt((currentPosition[0] - prevPosition[0]) * (currentPosition[0] - prevPosition[0]) + (currentPosition[1] - prevPosition[1]) * (currentPosition[1] - prevPosition[1]))
        self.textDistToPrev.SetValue(str(dist))
        
    def onTextRasterSize(self, event):
        size = int(self.textSize.GetValue())
        
        rasterSizeEvent = RasterResizeEvent(attr1 = size)
        wx.PostEvent(self.parent, rasterSizeEvent)
    
    def displayPolygon(self):
        polygonResetEvent = PolygonResetEvent(attr1 = self.getPolygonAsPointPairs())
        wx.PostEvent(self.parent, polygonResetEvent)
            
    def getPolygonAsPointPairs(self):
        text = self.textOutput.GetValue()
        
        tokens = text.split(',')
        result = []
        for x, y in zip(tokens[0::2], tokens[1::2]):
            result.append([int(float(x)), int(float(y))])
        
        return result
        
    def displayNofPoints(self):
        self.textNofPoints.SetValue(str(self.nofPoints))
    
    def getFormated(self, val):
        formated = ""
        type = self.comboOutType.GetStringSelection()
        
        if "double" == type:
            formated = str(val) + "."
        elif "float" == type:
            formated = str(val) + ".f"
        elif "int" == type:
            formated = str(val)
        
        return formated 