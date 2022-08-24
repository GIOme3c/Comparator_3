import wx
from wx import HORIZONTAL,VERTICAL
from debug import timer
from SettingsPanel import SettingsPanel
from Content import ContentTable
import HTMLManager, OptionsManager

class MainWindow(wx.Frame):
    #@timer
    def __init__(self, parent):
        super().__init__(parent, title = "Comparator", style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)

        self.content_table = ContentTable()
        self.Browser = self.content_table.CreateBrowser(self)   

        sizer = self.sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(self.sizer)
        
        self.log = self.CreateStatusBar(1)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        options = OptionsManager.getOptions()
        self.SettingsPanel = SettingsPanel(self, self.content_table, options)
        self.content_table.set_sPanel(self.SettingsPanel, options)

        sizer.Add(self.SettingsPanel, 0, wx.EXPAND, 0)
        sizer.Add(self.Browser, 1, wx.EXPAND ,0)


    #@timer
    def onClose(self, event):
        event.Skip()


if __name__ == '__main__':
    WX_APP = wx.App()
    WINDOW = MainWindow(None)
    WINDOW.Show()
    WX_APP.MainLoop()
    HTMLManager.END()