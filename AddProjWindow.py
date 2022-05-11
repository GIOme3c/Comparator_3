import wx
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class ListPanel(wx.Panel):
    def __init__(self, parent, projects):
        super().__init__(parent = parent)

        panel_sizer = wx.FlexGridSizer(cols = 2, vgap = 3, hgap = 5)
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

        for name in projects:
            STName = wx.StaticText(
                self,
                label = name,
            )
            STPath = wx.StaticText(
                self,
                label = projects[name],
            )
            panel_sizer.Add(STName, 0, wx.EXPAND | wx.LEFT, 5)
            panel_sizer.Add(STPath, 0, wx.EXPAND | wx.LEFT, 5)

class MainPanel(wx.Panel):
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
        ok_button = wx.Button(
            self,
            label = "OK",
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
            (ok_button,0,wx.RIGHT,25),
            (cancel_button,0,wx.LEFT,25),
        ])
        panel_sizer.AddMany([
            (select_dir,0,wx.ALIGN_CENTER | wx.TOP,20),
            (name_as_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (close_button_sizer,0,wx.ALIGN_CENTER | wx.TOP,50),
        ])

        select_dir.Bind(wx.EVT_DIRPICKER_CHANGED, self.onSelect)
        ok_button.Bind(wx.EVT_BUTTON, self.onOK)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)

    def onOK(self,event):
        parent = self.GetParent()
        parent.name = self.name_as.GetValue()
        parent.retCode = 1
        parent.Close()

    def onCancel(self,event):
        parent = self.GetParent()
        parent.retCode = 0
        parent.Close()

    def onSelect(self,event):
        parent = self.GetParent()
        parent.path = event.GetPath()
        slash_pos = parent.path.rfind('\\')
        auto_name = parent.path[slash_pos+1:]
        self.name_as.SetLabel(auto_name)
        parent.name = auto_name

class MainSizer(wx.BoxSizer):
    def __init__(self, parent, projects):
        super().__init__(VERTICAL)

        self.Add(MainPanel(parent), 1, wx.EXPAND, 5)
        self.Add(ListPanel(parent, projects), 2, wx.EXPAND, 5)

class AddProjectWindow(wx.Dialog):
    def __init__(self, parent, projects):
        super().__init__(parent, title = "Select project", size = (500, 600))

        self.path = "None"
        self.name = ""
        self.retCode = 0
        self.SetSizer(MainSizer(self,projects))
        self.Layout()

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        # print(self.path, self.select, self.retCode)
        self.EndModal(self.retCode)
        # event.Skip()