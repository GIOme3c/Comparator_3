import wx
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class MainPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        parent = self.GetParent()
        panel_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(panel_sizer)
        # self.SetBackgroundColour(wx.Colour(100,100,100))
        close_button_sizer = wx.BoxSizer(HORIZONTAL)
        select_main_sizer = wx.BoxSizer(HORIZONTAL)
        select_sub_sizer = wx.BoxSizer(HORIZONTAL)

       
        select_main_label = wx.StaticText(
            self,
            label = "Select main",
        )
        select_main_label.SetFont(CL.FONT_10)
        select_main_choise = wx.Choice(
            self,
            choices = list(self.GetParent().project_list)
        )
        select_main_choise.SetSelection(0)
        parent.main_select = select_main_choise.GetStringSelection()

        select_sub_label = wx.StaticText(
            self,
            label = "Select sub",
        )
        select_sub_label.SetFont(CL.FONT_10)
        select_sub_choise = wx.Choice(
            self,
            choices = list(self.GetParent().project_list)
        )
        select_sub_choise.SetSelection(0)
        parent.sub_select = select_sub_choise.GetStringSelection()

        ok_button = wx.Button(
            self,
            label = "OK",
        )
        cancel_button = wx.Button(
            self,
            label = "Cancel",
        )

        select_main_sizer.AddMany([
            (select_main_label,0,wx.TOP,3),
            (select_main_choise,0,wx.LEFT,5),
        ])
        select_sub_sizer.AddMany([
            (select_sub_label,0,wx.TOP,3),
            (select_sub_choise,0,wx.LEFT,5),
        ])
        close_button_sizer.AddMany([
            (ok_button,0,wx.RIGHT,25),
            (cancel_button,0,wx.LEFT,25),
        ])
        panel_sizer.AddMany([
            (select_main_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (select_sub_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (close_button_sizer,0,wx.ALIGN_CENTER | wx.TOP,50),
        ])


        select_main_choise.Bind(wx.EVT_CHOICE, self.onChoiceMain)
        select_sub_choise.Bind(wx.EVT_CHOICE, self.onChoiceSub)
        ok_button.Bind(wx.EVT_BUTTON, self.onOK)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)

    def onOK(self,event):
        parent = self.GetParent()
        parent.retCode = 1
        parent.Close()

    def onCancel(self,event):
        parent = self.GetParent()
        parent.retCode = 0
        parent.Close()

    def onChoiceMain(self,event):
        parent = self.GetParent()
        parent.main_select = event.GetString()
    
    def onChoiceSub(self,event):
        parent = self.GetParent()
        parent.sub_select = event.GetString()


class MainSizer(wx.BoxSizer):
    def __init__(self, parent):
        super().__init__(VERTICAL)

        self.Add(MainPanel(parent), 1, wx.EXPAND, 5)

class AddCompareWindow(wx.Dialog):
    def __init__(self, parent, project_list):
        super().__init__(parent, title = "Create compare")

        self.project_list = project_list
        self.main_select = ""
        self.sub_select = ""
        self.retCode = 0
        self.SetSizer(MainSizer(self))

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.EndModal(self.retCode)