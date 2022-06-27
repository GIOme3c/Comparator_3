import wx, os
from debug import timer
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class ListPanel(wx.Panel):
    @timer
    def __init__(self, parent):
        super().__init__(parent = parent)

        panel_sizer = self.panel_sizer = wx.FlexGridSizer(cols = 2, vgap = 3, hgap = 5)
        self.SetSizer(panel_sizer)

        STNameHeader = wx.StaticText(
            self,
            label = "Name",
        )
        STNameHeader.SetBackgroundColour(CL.COLOUR[CL.HEADER])
        STPathHeader = wx.StaticText(
            self,
            label = "Path",
        )
        STPathHeader.SetBackgroundColour(CL.COLOUR[CL.HEADER])
        panel_sizer.Add(STNameHeader, 0, wx.EXPAND | wx.LEFT, 5)
        panel_sizer.Add(STPathHeader, 0, wx.EXPAND | wx.LEFT, 5)

        for name in parent.projects:
            STName = wx.StaticText(
                self,
                label = name,
            )
            STPath = wx.StaticText(
                self,
                label = parent.projects[name],
            )
            panel_sizer.Add(STName, 0, wx.EXPAND | wx.LEFT, 5)
            panel_sizer.Add(STPath, 0, wx.EXPAND | wx.LEFT, 5)
    
    @timer
    def addProject(self,name,path):
        STName = wx.StaticText(
            self,
            label = name,
        )
        STPath = wx.StaticText(
            self,
            label = path,
        )
        self.panel_sizer.Add(STName, 0, wx.EXPAND | wx.LEFT, 5)
        self.panel_sizer.Add(STPath, 0, wx.EXPAND | wx.LEFT, 5)
        self.GetParent().Layout()

class MainPanel(wx.Panel):
    @timer
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        panel_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(panel_sizer)
        # self.SetBackgroundColour(wx.Colour(100,100,100))
        name_as_sizer = wx.BoxSizer(HORIZONTAL)
        close_button_sizer = wx.BoxSizer(HORIZONTAL)

        select_dir = wx.DirPickerCtrl(
            self,
        )
        name_as_label = wx.StaticText(
            self,
            label = "Name as",
        )
        name_as_label.SetFont(CL.FONT_10)
        name_as_field = self.name_as = wx.TextCtrl(
            self,
        )
        add_button = wx.Button(
            self,
            label = "Add",
        )
        cancel_button = wx.Button(
            self,
            label = "Cancel",
        )

        name_as_sizer.AddMany([
            (name_as_label,0,wx.TOP,3),
            (name_as_field,0,wx.LEFT,5),
        ])
        close_button_sizer.AddMany([
            (add_button,0,wx.RIGHT,25),
            (cancel_button,0,wx.LEFT,25),
        ])
        panel_sizer.AddMany([
            (select_dir,0,wx.ALIGN_CENTER | wx.TOP,20),
            (name_as_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (close_button_sizer,0,wx.ALIGN_CENTER | wx.TOP,50),
        ])

        select_dir.Bind(wx.EVT_DIRPICKER_CHANGED, self.onSelect)
        add_button.Bind(wx.EVT_BUTTON, self.onAdd)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)

    @timer
    def onAdd(self,event):
        parent = self.GetParent()
        grand = parent.GetParent()
        parent.name = self.name_as.GetValue()

        if os.path.isdir(parent.path):
            grand.content_table.AddProject(parent.name,parent.path)
            parent.lPanel.addProject(parent.name,parent.path)
        # parent.retCode = 1
        # parent.Close()

    @timer
    def onCancel(self,event):
        parent = self.GetParent()
        parent.retCode = 0
        parent.Close()
    
    @timer
    def onSelect(self,event):
        parent = self.GetParent()
        parent.path = event.GetPath()
        slash_pos = parent.path.rfind('\\')
        auto_name = parent.path[slash_pos+1:]
        self.name_as.SetLabel(auto_name)
        parent.name = auto_name

class AddProjectWindow(wx.Dialog):
    @timer
    def __init__(self, parent, projects):
        super().__init__(parent, title = "Select project", size = (500, 600))

        self.projects = projects

        self.path = "None"
        self.name = ""
        self.retCode = 0
        main_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(main_sizer)

        self.mPanel = MainPanel(self)
        self.lPanel = ListPanel(self)

        main_sizer.Add(self.mPanel, 1, wx.EXPAND, 5)
        main_sizer.Add(self.lPanel, 2, wx.EXPAND, 5)

        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose)
    
    @timer
    def onClose(self, event):
        # print(self.path, self.select, self.retCode)
        self.EndModal(self.retCode)
        # event.Skip()