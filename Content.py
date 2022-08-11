
import wx.html2, re, FileManager, HTMLManager
import ConstantLib as CL
from debug import timer


class ContentTable(list):

    def __init__(self):
        super().__init__()
        self.browser = None
        self.projects = {}
        self.compares = []
        self.headers = []
        self.files = []
        self.last_id = -1
        self.json = {}
        self.settings = {}

    def append_header(self,header,colour):
        new_header = HeaderRow(self,header,colour)
        self.headers.append(new_header)
        super().append(new_header)


    def Refresh(self):
        newFiles = []
        for compare in self.compares:
            mainS, subS = compare
            self.projects[mainS],mFiles = FileManager.GetFiles(self.projects[mainS])
            self.projects[subS],sFiles = FileManager.GetFiles(self.projects[subS])
            newFiles = FileManager.ConcatLists([mFiles,sFiles,newFiles])
        
        for row in self:
            row.Refresh()

        for file in newFiles:
            if file not in self.files:
                self.append(file)
        
        self.ShowNewData()

    def set_sPanel(self,sPanel):
        self.sPanel = sPanel
        self.GetCurrentSettings()

    def getId(self):
        self.last_id += 1
        return self.last_id

    def append(self,file):
        self.files.append(file)
        super().append(ContentRow(file, self.compares, self))

    #@timer
    def CreateBrowser(self, parent):
        self.browser = wx.html2.WebView.New(parent = parent, backend = wx.html2.WebViewBackendEdge, url = CL.BASE_URL) 

        HTMLManager.setStartPage()
        return self.browser

    def AddProject(self,pName,pPath):
        self.projects[pName] = pPath

    #@timer
    def AddCompare(self,compare): 

        if compare in self.compares:
            return
        
        #@timer
        def AddCol(compare):
            for row in self:
                row.append(compare)

        #@timer
        def AddFiles(files):
            for file in files:
                if file not in self.files:
                    self.append(file)

        mainS,subS = compare[0],compare[1]
        self.compares.append(compare)
        AddCol(compare)

        self.projects[mainS],mFiles = FileManager.GetFiles(self.projects[mainS])
        self.projects[subS],sFiles = FileManager.GetFiles(self.projects[subS])
        newFiles = FileManager.ConcatLists([mFiles,sFiles])
        AddFiles(newFiles)

    def ShowNewData(self): #!Rewrite!!
        HTMLManager.setContentPage(self.getHtml())
        HTMLManager.setData(self.json)
        self.browser.Reload()

    def getHead(self):
        html = "<thead>\n<tr>\n<th data-rtc-resizable = 'files'>Files</th>\n"
        for compare in self.compares:
            html += f"<th  data-rtc-resizable ='{compare[0]}&{compare[1]}' >{compare[0]} & {compare[1]}</th>\n"
        html += "</tr>\n</thead>\n"
        return html

    def getHtml(self):
        self.sort()
        html = "<table id = 'main_table' class='data' data-rtc-resizable-table='main_table'>"
        html += self.getHead()
        for el in self:
            html+= el.getHtml()
        html+="</table>"

        return html
    
    def GetCurrentSettings(self):
        self.settings['WL'] = self.sPanel.white_list
        self.settings['BL'] = self.sPanel.black_list
        self.settings['WLC'] = self.sPanel.WL_check.GetValue()
        self.settings['BLC'] = self.sPanel.BL_check.GetValue()
        self.settings['AEC'] = self.sPanel.AE_check.GetValue()
        self.settings['CEC'] = self.sPanel.CE_check.GetValue()

    def CheckNewRules(self):
        self.GetCurrentSettings()
        for row in self:
            row.checkRules()
        HTMLManager.setContentPage(self.getHtml())
        self.browser.Reload()


class HeaderRow():

    def __init__(self,parent,file_name,colour) -> None:
        self.file_name = file_name
        self.parent = parent
        self.colour = colour

    def __str__(self):
        return self.file_name

    def __lt__(self, x) -> bool:
        return self.file_name<x.file_name
    
    def __gt__(self, x) -> bool:
        return self.file_name>x.file_name

    def Refresh(self):
        pass

    def append(self):
        pass

    def getHtml(self):
        rgb = self.colour.Get()
        return f"<tr> <td style = 'background-color: rgb({rgb[0]},{rgb[1]},{rgb[2]});' colspan='{len(self.parent.compares)+1}'>{self.file_name}</td> </tr>"

    def checkRules(self):
        pass


class ContentRow(list):

    def __init__(self, file, compares, parent):
        super().__init__()
        self.file_name = file
        self.compares = compares
        self.parent = parent
        self.settings = parent.settings
        self.html = ["<tr>",f'<td class = "file_name">{self.file_name}</td>',"</tr>"]
        for compare in compares:
            self.append(compare)
        self.checkRules()
        
    def __str__(self):
        return self.file_name

    def __lt__(self, x) -> bool:
        return self.file_name<x.file_name
    
    def __gt__(self, x) -> bool:
        return self.file_name>x.file_name
    
    def checkRules(self):
        self.html[0] = f"<tr {'hidden'*(not self.ShowRow())}>"

    def Refresh(self):
        for cell in self:
            cell.setData()
    
    def updateHtml(self,a,b):
        i = self.html.index(a)
        self.html[i] = b

    def addHtml(self,a):
        self.html.insert(-1,a)

    def getHtml(self):
        return '\n'.join(self.html)

    def updateJson(self,uid, data):
        self.parent.json[uid] = data

    def getId(self):
        return self.parent.getId()

    def append(self,compare):
        super().append(ContentCell(self.file_name,compare,self))

    def path_control(self, path, rules):
        for rule in rules:
            try:
                compare_result = re.search(rule, path)
            except:
                continue
            if (compare_result != None):
                if (compare_result.group(0)!=''):
                    return False
        return True

    def CheckAE(self):
        all_exist = True
        for cell in self:
            if cell.type != CL.EXISTS:
                all_exist = False
                break
        if all_exist == True and self.settings['AEC'] == False:
            return False
        else:
            return True

    def CheckCE(self):
        compare_error = False
        for cell in self:
            if cell.type == CL.COMPERR:
                compare_error = True
                break
        if compare_error == True and self.settings['CEC'] == False:
            return False
        else:
            return True

    def CheckBL(self):
        if self.settings['BLC'] == False:
            return True
        else:
            return self.path_control(self.file_name,self.settings['BL'])

    def CheckWL(self):
        if self.settings['WLC'] == False:
            return True
        else:
            return not self.path_control(self.file_name,self.settings['WL'])
    
    def ShowRow(self):
        return self.CheckAE() and self.CheckCE() and self.CheckBL() and self.CheckWL()
        

class ContentCell():

    #@timer
    def __init__(self,file, compare, parent) -> None:
        self.file = file
        self.compare = (parent.parent.projects[compare[0]],parent.parent.projects[compare[1]])
        self.uid = parent.getId()
        self.parent = parent
        self.html = None
        self.setData()

    def setData(self):
        mFile, sFile = self.compare[0]+self.file, self.compare[1]+self.file
        mState, sState = FileManager.CompareFiles(mFile, sFile)
        if (mState == sState == CL.MISSING):
            self.type = CL.EMPTY
        elif (mState == CL.COMPERR or sState == CL.COMPERR):
            self.type = CL.COMPERR
        else:
            self.type = sState


        if self.type == CL.EXISTS:
            self.text = FileManager.GetText(mFile, True)
        elif self.type == CL.DIFFERS:
            if (mState != CL.MISSING):
                self.text = FileManager.GetDifferens(mFile, sFile)
            else:
                self.text = FileManager.GetText(sFile, True)
        elif self.type == CL.MISSING:
            self.text = FileManager.GetText(mFile, True)
        elif self.type == CL.COMPERR:
            self.text = "The file has an unreadable type"
        elif self.type == CL.EMPTY:
            self.text = "The file is missing in both projects"    

        self.toJSON() 
        self.toHTML() 

    #@timer
    def toJSON(self):
        self.json = {"rows":[], "types":[]}
        if type(self.text) == str:
            self.json["rows"].append(self.text.replace('<','&lt').replace('>','&gt').replace('\n','<br>'))
            self.json["types"].append(CL.TYPES[self.type])
        else:
            for line in self.text:
                if (line[:2] != '? '):
                    self.json["types"].append(CL.TYPES[line[:2]])
                    self.json["rows"].append(line[2:].replace('<','&lt').replace('>','&gt'))
        self.parent.updateJson(self.uid, self.json)

    #@timer
    def toHTML(self):
        newHTML = f'<td code="{self.uid}" class = {self.type}>{self.type}</td>'
        if self.html:
            self.parent.updateHtml(self.html, newHTML)
        else:
            self.parent.addHtml(newHTML)
        self.html = newHTML

            
if __name__ == "__main__":
    a = ContentTable()
