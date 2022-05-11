
import wx.html2
import ConstantLib as CL
import FileManager
import HTMLManager

class ContentTable():
    browser = None
    projects = {}
    compares = []
    files = []

    cols = 1
    raws = 0
    table = [[]]
    
    def __init__(self) -> None:
        self.table[0].append(Cell(
            type = CL.HEADER,
            label = 'File path',
        ))
    
    def CreateBrowser(self, parent):
        self.browser = wx.html2.WebView.New(parent = parent, backend = wx.html2.WebViewBackendEdge, url = CL.BASE_URL) 
        HTMLManager.setStartPage()
        return self.browser

    def AddRow(self, file_name):
        self.table.append([Cell(
            type = CL.FNAME,
            label = file_name,
        )])
        
        for compare in self.compares:
            main_project = self.projects[compare[0]]
            sub_project = self.projects[compare[1]]
            
            self.table[-1].append(Cell(
                compare = (main_project,sub_project),
                file = file_name,
            ))

    def AddCol(self, compare):
        compare_name = compare[0]+' && '+compare[1]
        self.table[0].append(Cell(
            label = compare_name,
            type = CL.HEADER,
        ))

        main_project = self.projects[compare[0]]
        sub_project = self.projects[compare[1]]
        for row in self.table[1:]:
            row.append(Cell(
                compare = (main_project,sub_project),
                file = row[0].label,
            ))

    def AddProject(self,pName,pPath):
        self.projects[pName] = pPath

    def AddCompare(self, mainS, subS): 
        compare = (mainS,subS)
        if compare in self.compares:
            return
        self.compares.append(compare)
        self.AddCol(compare)

        self.projects[mainS],mFiles = FileManager.GetFiles(self.projects[mainS])
        self.projects[subS],sFiles = FileManager.GetFiles(self.projects[subS])
        newFiles = FileManager.ConcatLists([mFiles,sFiles])

        for file in newFiles:
            if file not in self.files:
                self.files.append(file)
                self.AddRow(file)

        HTMLManager.setContentPage(self.toHTML())
        self.browser.Reload()

    def toHTML(self):
        result = '<table>\n'
        result += self.RowToHTML(self.table[0], True)

        for row in self.table[1:]:
            result += self.RowToHTML(row, False)

        result += '\t</table>\n'

        return result


    def RowToHTML(self,row, head):
        margin = 2
        t = '\t'
        if (head):
            result = f'{t*margin}<thead>\n'
            margin += 1
        else:
            result = ''
        result += f'{t*margin}<tr>\n'
        for cell in row:
            result += cell.toHTML(margin+1)
        result += f'{t*margin}</tr>\n'
        if (head):
            margin-=1
            result += f'{t*margin}</thead>\n'
        return result

class Cell():
    label = 'File path'
    type = CL.HEADER
    text = None

    def __init__(self, label = None, type = None, compare = None, file = None) -> None:
        self.label = label
        self.type = type
        self.file = file
        self.compare = compare

        if type != None:
            return

        mFile, sFile = compare[0]+file, compare[1]+file
        mState, sState = FileManager.CompareFiles(mFile, sFile)
        if (mState == sState == CL.MISSING):
            self.type = self.label = CL.EMPTY
        elif (mState == CL.COMPERR or sState == CL.COMPERR):
            self.type = self.label = CL.COMPERR
        else:
            self.type = self.label = sState

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

    def toHTML(self,margin):
        t = '\t'
        return f"{t*margin}<td class = {self.type}>\n{t*(margin+1)}<div>{self.label}</div>\n{t*margin}</td>\n"