import wx
from wx import HORIZONTAL,VERTICAL
from SettingsPanel import SettingsPanel
import HTMLManager
from ContentTable import ContentTable

class MainWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title = "Comparator", style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)

        self.content_table = ContentTable()
        self.Browser = self.content_table.CreateBrowser(self)   

        sizer = self.sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(self.sizer)
        
        self.log = self.CreateStatusBar(1)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.SettingsPanel = SettingsPanel(self, self.content_table)

        sizer.Add(self.SettingsPanel, 0, wx.EXPAND, 0)
        sizer.Add(self.Browser, 1, wx.EXPAND ,0)


    def onClose(self, event):
        event.Skip()


if __name__ == '__main__':
    WX_APP = wx.App()
    WINDOW = MainWindow(None)
    WINDOW.Show()
    WX_APP.MainLoop()
    HTMLManager.END()