import wx
from wx import HORIZONTAL,VERTICAL
from ConstantLib import HSIZE,VSIZE
from debug import timer


class SelectListWindow(wx.Dialog):
    @timer
    def __init__(self, parent, title, cList):
        super().__init__(parent = parent, title = title, size = (int(HSIZE()/3),int(VSIZE()/2)))

        self.retCode = 0
        main_sizer = wx.BoxSizer(VERTICAL)
        close_button_sizer = wx.BoxSizer(HORIZONTAL)
        select_sizer = wx.BoxSizer(HORIZONTAL)
        self.SetSizer(main_sizer)

        select_text = wx.StaticText(
            self,
            label = self.GetTitle().replace("Edit","Select"),
        )
        select_file = wx.FilePickerCtrl(
            self,
        )
        edit_text = wx.StaticText(
            self,
            label = self.GetTitle(),
        )
        edit_field = self.edit_field = wx.TextCtrl(
            self,
            style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH,
        )
        ok_button = wx.Button(
            self,
            label = "OK",
        )
        cancel_button = wx.Button(
            self,
            label = "Cancel",
        )

        select_sizer.AddMany([
            (select_text,0,wx.TOP,3),
            (select_file,0,wx.LEFT,10),
        ])
        close_button_sizer.AddMany([
            (ok_button,0,wx.RIGHT,40),
            (cancel_button,0,wx.LEFT,40),
        ])
        main_sizer.AddMany([
            (select_sizer,0,wx.ALIGN_CENTER | wx.TOP,20),
            (edit_text,0,wx.ALIGN_LEFT | wx.TOP, 20),
            (edit_field,1,wx.EXPAND,0),
            (close_button_sizer,0,wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM,10),
        ])

        select_file.Bind(wx.EVT_FILEPICKER_CHANGED, self.onSelect)
        ok_button.Bind(wx.EVT_BUTTON, self.onOK)
        cancel_button.Bind(wx.EVT_BUTTON, self.onCancel)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.initEditPanel(cList)

    @timer
    def initEditPanel(self, cList):
        self.rList = cList
        for el in cList:
            self.edit_field.AppendText(el+'\n')
    
    @timer
    def onSelect(self,event):
        path = event.GetPath()
        text = ""
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
        self.edit_field.SetValue(text)
    
    @timer
    def onOK(self,event):
        self.rList = self.StrToList(self.edit_field.GetValue())
        self.retCode = 1
        self.Close()

    @timer
    def onCancel(self,event):
        self.retCode = 0
        self.Close()

    @timer
    def onClose(self, event):
        self.EndModal(self.retCode)
        
    @timer
    def StrToList(self, someStr):
        someList = someStr.split('\n')
        i = 0
        while i<len(someList):
            someList[i] = someList[i].strip()
            if (someList[i] == ''):
                del someList[i]
            else:
                i+=1
        
        return someList

