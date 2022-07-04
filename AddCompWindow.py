import wx
from debug import timer
from wx import HORIZONTAL,VERTICAL
import ConstantLib as CL

class MainPanel(wx.Panel):
    #@timer
    def __init__(self, parent, compares, project_list):
        super().__init__(parent)

        self.compares = compares
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
        select_main_choise = self.select_main_choise = wx.Choice(
            self,
            choices = list(project_list)
        )
        select_main_choise.SetSelection(0)

        select_sub_label = wx.StaticText(
            self,
            label = "Select sub",
        )
        select_sub_label.SetFont(CL.FONT_10)
        select_sub_choise = self.select_sub_choise = wx.Choice(
            self,
            choices = list(project_list)
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

        ok_button.Bind(wx.EVT_BUTTON, self.onOK)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)

    #@timer
    def onOK(self,event):
        lPanel = self.GetParent().list_panel
        new_compare = (self.select_main_choise.GetStringSelection(), self.select_sub_choise.GetStringSelection())
        if new_compare not in self.compares:
            self.compares.append(new_compare)
            lPanel.add_compare(new_compare)

    #@timer
    def onCancel(self,event):
        parent = self.GetParent()
        parent.Close()

class ListPanel(wx.Panel):
    def __init__(self, parent, compares):
        super().__init__(parent)
        
        # self.isShown = []
        self.compares = compares
        panel_sizer = self.panel_sizer = wx.FlexGridSizer(cols = 2, vgap = 3, hgap = 5)
        self.SetSizer(panel_sizer)

        self.refresh()

    def refresh(self):
        self.panel_sizer.Clear(delete_windows=True)
        for compare in self.compares:
            # if compare not in self.isShown:
            self.add_compare(compare, False)

    def add_compare(self, compare, isNew = True):
        new_text = wx.StaticText(
            self,
            label = compare[0]+ ' & ' + compare[1],
        )
        new_button = wx.Button(
            self,
            label = "remove"
        )
        self.panel_sizer.Add(new_text, 0, wx.EXPAND | wx.LEFT, 5)
        self.panel_sizer.Add(new_button, 0, wx.EXPAND | wx.LEFT, 5)
        self.GetParent().Layout()
        if isNew:
            self.GetParent().new_compares.append(compare)
            print(f"NEW {compare}")

        # def delete_text(event):
        #     idx = self.compares.index(compare)
        #     self.compares.remove(compare)
        #     # self.panel_sizer.
        #     self.panel_sizer.Remove(idx)
        #     # new_text.Destroy()
        #     new_text = None
        #     self.panel_sizer.Remove(idx)
        #     # new_button.Destroy()
        #     new_button = None
        #     self.GetParent().Layout()
        
        # self.Bind(wx.EVT_BUTTON, delete_text, new_button)
        

class AddCompareWindow(wx.Dialog):
    def __init__(self, parent, project_list, compares):
        super().__init__(parent, title = "Create compare", size = (500, 600))

        self.new_compares = []
        self.main_sizer = wx.BoxSizer(VERTICAL)
        self.main_panel = MainPanel(self, compares,project_list)
        self.list_panel = ListPanel(self, compares)
        self.main_sizer.Add(self.main_panel, 1, wx.EXPAND, 5)
        self.main_sizer.Add(self.list_panel, 2, wx.EXPAND, 5)


        self.SetSizer(self.main_sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.EndModal(1)


# if __name__ == "__main__":
#     WX_APP = wx.App()
#     WINDOW = AddCompareWindow(
#         None,
#         ["1","2","3","4"],
#         [],
#     )
#     WINDOW.Show()
#     WX_APP.MainLoop()
    