from random import random
import wx, os
from debug import timer
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class ListPanel(wx.Panel):
    #@timer
    def __init__(self, parent,content):
        super().__init__(parent)
        self.content = content

        panel_sizer = self.panel_sizer = wx.FlexGridSizer(cols = 2, vgap = 3, hgap = 5)
        self.SetSizer(panel_sizer)

        STPathHeader = wx.StaticText(
            self,
            label = "Name",
        )
        STPathHeader.SetBackgroundColour(CL.COLOUR[CL.HEADER])
        CLPickerHeader = wx.StaticText(
            self,
            label = "Path",
        )
        CLPickerHeader.SetBackgroundColour(CL.COLOUR[CL.HEADER])
        panel_sizer.Add(STPathHeader, 0, wx.EXPAND | wx.LEFT, 5)
        panel_sizer.Add(CLPickerHeader, 0, wx.EXPAND | wx.LEFT, 5)

        for path in content.headers:
            STPath = wx.StaticText(
                self,
                label = path.file_name,
            )
            CLPicker = wx.ColourPickerCtrl(
                self,
                colour =path.colour,

            )
            panel_sizer.Add(STPath, 0, wx.EXPAND | wx.LEFT, 5)
            panel_sizer.Add(CLPicker, 0, wx.EXPAND | wx.LEFT, 5)
    
    #@timer
    def showHead(self):
        path = self.content.headers[-1]
        STPath = wx.StaticText(
            self,
            label = path.file_name,
        )
        CLPicker = wx.ColourPickerCtrl(
            self,
            colour =path.colour,

        )
        self.panel_sizer.Add(STPath, 0, wx.EXPAND | wx.LEFT, 5)
        self.panel_sizer.Add(CLPicker, 0, wx.EXPAND | wx.LEFT, 5)
        self.GetParent().Layout()

class MainPanel(wx.Panel):
    #@timer

    def getRandomColour(self):
        r = int(random()*255)
        g = int(random()*255)
        b = int(random()*255)
        return wx.Colour(r,g,b)

    def __init__(self, parent, content):
        super().__init__(parent)
        
        self.content = content
        self.is_correct = False

        panel_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(panel_sizer)
        color_picker_sizer = wx.BoxSizer(HORIZONTAL)
        close_button_sizer = wx.BoxSizer(HORIZONTAL)

        select_dir = wx.DirPickerCtrl(
            self,
        )
        color_label = wx.StaticText(
            self,
            label = "Select color",
        )
        color_label.SetFont(CL.FONT_10)
        color_picker = self.color_picker = wx.ColourPickerCtrl(
            self,
            colour=self.getRandomColour()
        )
        add_button = wx.Button(
            self,
            label = "Add",
        )
        cancel_button = wx.Button(
            self,
            label = "Cancel",
        )

        color_picker_sizer.AddMany([
            (color_label,0,wx.TOP,3),
            (color_picker,0,wx.LEFT,5),
        ])
        close_button_sizer.AddMany([
            (add_button,0,wx.RIGHT,25),
            (cancel_button,0,wx.LEFT,25),
        ])
        panel_sizer.AddMany([
            (select_dir,0,wx.ALIGN_CENTER | wx.TOP,20),
            (color_picker_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (close_button_sizer,0,wx.ALIGN_CENTER | wx.TOP,50),
        ])

        select_dir.Bind(wx.EVT_DIRPICKER_CHANGED, self.onSelect)
        add_button.Bind(wx.EVT_BUTTON, self.onAdd)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)

    #@timer
    def onAdd(self,event):
        if self.is_correct:        
            self.content.append_header(self.path, self.color_picker.GetColour())
            parent = self.GetParent()
            parent.lPanel.showHead()
        

    #@timer
    def onCancel(self,event): 
        parent = self.GetParent()
        parent.retCode = 0
        parent.Close()
    
    #@timer
    def onSelect(self,event):
        self.is_correct = False
        self.path = event.GetPath().replace('\\','/')
        for root in self.content.projects:
            self.content.projects[root] = self.content.projects[root].replace('\\','/')
            if self.content.projects[root] in self.path:
                self.is_correct = True
                self.path = self.path.replace(self.content.projects[root],'')


class HeaderWindow(wx.Dialog):
    #@timer
    def __init__(self, parent, content):
        super().__init__(parent, title = "Add header", size = (500, 600))

        self.retCode = 0
        main_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(main_sizer)

        self.mPanel = MainPanel(self, content)
        self.lPanel = ListPanel(self, content)

        main_sizer.Add(self.mPanel, 1, wx.EXPAND, 5)
        main_sizer.Add(self.lPanel, 2, wx.EXPAND, 5)

        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose)
    
    #@timer
    def onClose(self, event):
        self.EndModal(self.retCode)
