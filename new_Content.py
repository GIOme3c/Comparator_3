
import wx.html2, re, FileManager, HTMLManager
import ConstantLib as CL
from debug import timer


class ContentTable(list):

    def __init__(self):
        super().__init__()
        self.browser = None
        self.projects = {}
        self.compares = []
        self.files = []
        self.last_id = -1
        self.json = {}

    def getId(self):
        self.last_id += 1
        return self.last_id

    def append(self,file):
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
        html = "<thead>\n<tr>\n"
        for compare in self.compares:
            html += f"<th>{compare[0]} & {compare[1]}</th>\n"
        html += "</tr>\n</thead>\n"
        return html



    def getHtml(self):
        html = "<table id = 'main_table' style = 'overflow:scroll'>"
        html += self.getHead()
        for el in self:
            html+= el.getHtml()
        html+="</table>"

        return html
    

class ContentRow(list):

    def __init__(self, file, compares, parent):
        super().__init__()
        self.file_name = file
        self.compares = compares
        self.parent = parent
        self.html = ["<tr>","</tr>"]
        for compare in compares:
            self.append(compare)
    
    def updateHtml(self,a,b):
        i = self.html.index(a)
        self.html[i] = b

    def addHtml(self,a):
        # self.html.append(a)
        self.html.insert(-1,a)

    def getHtml(self):
        return '\n'.join(self.html)

    def updateJson(self,uid, data):
        self.parent.json[uid] = data

    def getId(self):
        return self.parent.getId()

    def append(self,compare):
        super().append(ContentCell(self.file_name,compare,self))

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
        # if self.text == None: #!OPTIMIZE
        #     return {}
        self.json = {self.uid : {"rows":[], "types":[]}}
        if type(self.text) == str:
            self.json[self.uid]["rows"].append(self.text.replace('<','&lt').replace('>','&gt').replace('\n','<br>'))
            self.json[self.uid]["types"].append(CL.TYPES[self.type])
        else:
            for line in self.text:
                if (line[:2] != '? '):
                    self.json[self.uid]["types"].append(CL.TYPES[line[:2]])
                    self.json[self.uid]["rows"].append(line[2:].replace('<','&lt').replace('>','&gt'))
        self.parent.updateJson(self.uid, self.json)

    #@timer
    def toHTML(self):
        newHTML = f'<td code="{self.uid}" class = {self.type}>{self.type}</td>\n'
        if self.html:
            self.parent.updateHtml(self.html, newHTML)
        else:
            self.parent.addHtml(newHTML)
        self.html = newHTML

            

   
if __name__ == "__main__":
    a = ContentTable()
