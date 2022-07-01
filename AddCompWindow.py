import wx
from debug import timer
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class MainPanel(wx.Panel):
    #@timer
    def __init__(self, parent):
        super().__init__(parent)

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

    #@timer
    def onOK(self,event):
        parent = self.GetParent()
        parent.retCode = 1
        parent.Close()

    #@timer
    def onCancel(self,event):
        parent = self.GetParent()
        parent.retCode = 0
        parent.Close()

class ListPanel(wx.Panel):
    def __init__(self, parent, compares):
        super().__init__(parent)
        
        self.compares = compares
        panel_sizer = self.panel_sizer = wx.FlexGridSizer(cols = 2, vgap = 3, hgap = 5)
        self.SetSizer(panel_sizer)

    def refresh(self):
        self.panel_sizer.Clear(delete_windows=True)
        for compare in self.compares:
            if compare not in self.isShown:
                self.add_compare(compare)

    def add_compare(self, compare):
        new_text = wx.StaticText(
            self,
            label = compare[0]+ ' & ' + compare[1],
        )
        new_button = wx.BoxSizer(
            self,
            label = "remove"
        )
        self.panel_sizer.Add(new_text)
        self.panel_sizer.Add(new_button)

        def delete_text(event):
            self.compares.remove(compare)
            self.panel_sizer.Detach(new_text)
            new_text.Destroy()
            new_text = None
            self.panel_sizer.Detach(new_button)
            new_button.Destroy()
            new_button = None
            self.GetParent.Layout()
        
        self.Bind(wx.EVT_BUTTON, delete_text, new_button)
        

        

class AddCompareWindow(wx.Dialog):
    def __init__(self, parent, project_list, compares):
        super().__init__(parent, title = "Create compare")

        self.project_list = project_list

        self.main_sizer = wx.BoxSizer(VERTICAL)
        self.main_panel = MainPanel(parent)
        self.list_panel = ListPanel(parent)
        self.main_sizer.Add(self.main_panel, 1, wx.EXPAND, 5)
        self.main_sizer.Add(self.list_panel, 2, wx.EXPAND, 5)


        self.SetSizer(self.main_sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.EndModal(self.retCode)