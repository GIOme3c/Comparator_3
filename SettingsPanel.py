import wx
from wx import HORIZONTAL,VERTICAL
from AddProjWindow import AddProjectWindow
from AddCompWindow import AddCompareWindow
from SelectList import SelectListWindow
from ExportWindow import ExportWindow
from HeaderWindow import HeaderWindow
from debug import timer



class SettingsPanel(wx.Panel):
    #@timer
    def __init__(self, parent, content_table):
        super().__init__(parent)

        self.content_table = content_table
        
        self.log = self.GetParent().log
        settings_sizer = wx.BoxSizer(HORIZONTAL)
        self.SetSizer(settings_sizer)
        self.white_list = []
        self.black_list = []

        addP_button = wx.Button(
            self,
            label = "ADD Project",
        )
        addC_button = wx.Button(
            self,
            label = "ADD Compare",
        )
        WL_button = wx.Button(
            self,
            label = "Edit White list",
        )
        BL_button = wx.Button(
            self,
            label = "Edit Black list",
        )
        refresh_button = wx.Button(
            self,
            label = "Refresh data",
        )
        header_button = wx.Button(
            self,
            label = "Add header",
        )
        export_button = wx.Button(
            self,
            label = "Export HTML",
        )

        WL_check = self.WL_check = wx.CheckBox(
            self,
            label = "White list",
        )
        BL_check = self.BL_check = wx.CheckBox(
            self,
            label = "Black list",
        )
        AE_check = self.AE_check = wx.CheckBox(
            self,
            label = "All exists",
        )
        CE_check = self.CE_check = wx.CheckBox(
            self,
            label = "Compare error",
        )

        settings_sizer.AddMany([
            (addP_button,),
            (addC_button,),
            (WL_button,),
            (WL_check,0,wx.TOP,3),
            (BL_button,),
            (BL_check,0,wx.TOP,3),
            (AE_check,0,wx.TOP,3),
            (CE_check,0,wx.TOP,3),
            (refresh_button),
            (header_button),
            (export_button),
        ])

        self.Bind(wx.EVT_BUTTON, self.onRefreshClick, refresh_button)  
        self.Bind(wx.EVT_BUTTON, self.onHeaderClick, header_button)  
        self.Bind(wx.EVT_BUTTON, self.onExportClick, export_button)
        self.Bind(wx.EVT_BUTTON, self.onAddPButtonClicked, addP_button)
        self.Bind(wx.EVT_BUTTON, self.onAddCButtonClicked, addC_button)
        self.Bind(wx.EVT_BUTTON, self.onEditWLClick, WL_button)
        self.Bind(wx.EVT_BUTTON, self.onEditBLClick, BL_button)
        self.Bind(wx.EVT_CHECKBOX, self.onCheckBoxClick) 

    def onHeaderClick(self,event):
        new_window = HeaderWindow(self,self.content_table)
        new_window.ShowModal()
        self.content_table.ShowNewData()

    #@timer
    def onExportClick(self,event):
        new_window = ExportWindow(self)
        new_window.ShowModal()

    def onCheckBoxClick(self,event):
        self.content_table.CheckNewRules()

    #@timer
    def onRefreshClick(self,event):
        self.content_table.Refresh()

    #@timer
    def onEditWLClick(self, event):
        newWindow = SelectListWindow(
            self,
            title = "Edit White list",
            cList = self.white_list,
        )
        if newWindow.ShowModal():
            self.white_list = newWindow.rList
            self.content_table.CheckNewRules()

    #@timer
    def onEditBLClick(self, event):
        newWindow = SelectListWindow(
            self,
            title = "Edit Black list",
            cList = self.black_list,
        )
        if newWindow.ShowModal():
            self.black_list = newWindow.rList
            self.content_table.CheckNewRules()

    #@timer
    def onAddPButtonClicked(self, event):
        add_project_window = AddProjectWindow(
            self,
            self.content_table.projects,
        )
        add_project_window.ShowModal()
        add_project_window.Destroy()

    #@timer
    def onAddCButtonClicked(self, event):
        add_compare_window = AddCompareWindow(
            self,
            self.content_table.projects,
            self.content_table.compares,
        )
        add_compare_window.ShowModal()
        for compare in add_compare_window.new_compares:
            self.content_table.AddCompare(compare)
        self.content_table.ShowNewData()
        add_compare_window.Destroy()