import wx, os, shutil
from wx import HORIZONTAL,VERTICAL

class ImportWindow(wx.Dialog):
    def __init__(self, parent) -> None:
        super().__init__(parent, title = "Import")

        dirpick_text = wx.StaticText(
            self,
            label = "Choise directory",
        )
        select_dir = self.select_dir = wx.DirPickerCtrl(
            self,
        )
        folder_name_text = wx.StaticText(
            self,
            label = "Write name of ipmort folder",
        )
        import_folder_name = self.import_folder_name = wx.TextCtrl(
            self,
            value = "New import",
        )
        import_button = wx.Button(
            self,
            label = "import",
        )
        cur_size = import_button.GetSize()
        import_button.SetMinSize((cur_size[0]*1.4,cur_size[1]*1.4))

        main_sizer = wx.BoxSizer(VERTICAL)
        self.SetSizer(main_sizer)
        main_sizer.AddMany([
            (dirpick_text,0,wx.ALIGN_CENTER | wx.TOP,20),
            (select_dir,0,wx.ALIGN_CENTER,10),
            (folder_name_text,0,wx.ALIGN_CENTER | wx.TOP,25),
            (import_folder_name,0,wx.ALIGN_CENTER,10),
            (import_button,0,wx.ALIGN_CENTER| wx.TOP,30),
        ])

        import_button.Bind(wx.EVT_BUTTON, self.onImportClick)

    def onImportClick(self, event):
        root_dir = self.select_dir.GetPath()
        new_folder_path =root_dir +'\\'+ self.import_folder_name.GetValue()
        if os.path.isdir(root_dir):
            if os.path.isdir(new_folder_path):
                pass #Exist now
            else:
                os.mkdir(new_folder_path)
                shutil.copyfile('content/content.html',new_folder_path+'/content.html')
                shutil.copyfile('content/data.json',new_folder_path+'/data.json')
                shutil.copyfile('content/script.js',new_folder_path+'/script.js')
                shutil.copyfile('content/style.css',new_folder_path+'/style.css')
                os.system(f"explorer {new_folder_path}")
                self.Close()
        else:
            pass #No Exist
