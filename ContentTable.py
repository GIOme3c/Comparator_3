
import wx.html2, re, FileManager, HTMLManager
import ConstantLib as CL

class ContentTable():
    browser = None
    projects = {}
    compares = []
    files = []
    last_id = -1
    
    def GetID(self):
        self.last_id+=1
        return self.last_id

    def __init__(self) -> None:
        self.Refresh()
    
    def Refresh(self):
        self.last_id = -1
        self.table = [[Cell(
            type = CL.HEADER,
            label = 'File path',
            uid = self.GetID(),
        )]]
        self.files = []
        old_compares = list(self.compares)
        self.compares = []

        for compare in old_compares:
            self.AddCompare(compare[0],compare[1])

    def CreateBrowser(self, parent):
        self.browser = wx.html2.WebView.New(parent = parent, backend = wx.html2.WebViewBackendEdge, url = CL.BASE_URL) 
        HTMLManager.setStartPage()
        # wx.html2.WebView.RunScript()
        # print(self.browser.RunScript())
        # print(self.browser.RunScript("console.log(a);"))
        return self.browser

    def AddRow(self, file_name):
        self.table.append([Cell(
            type = CL.FNAME,
            label = file_name,
            uid = self.GetID(),
        )])
        
        for compare in self.compares:
            main_project = self.projects[compare[0]]
            sub_project = self.projects[compare[1]]
            
            self.table[-1].append(Cell(
                compare = (main_project,sub_project),
                file = file_name,
                uid = self.GetID(),
            ))

    def AddCol(self, compare):
        compare_name = compare[0]+' && '+compare[1]
        self.table[0].append(Cell(
            label = compare_name,
            type = CL.HEADER,
            uid = self.GetID(),
        ))

        main_project = self.projects[compare[0]]
        sub_project = self.projects[compare[1]]
        for row in self.table[1:]:
            row.append(Cell(
                compare = (main_project,sub_project),
                file = row[0].label,
                uid = self.GetID(),
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

    def ShowNewData(self):
        HTMLManager.setContentPage(self.toHTML())
        HTMLManager.setData(self.new_json)
        self.browser.Reload()

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

    def CheckAE(self, row):
        all_exist = True
        for cell in row[1:]:
            if cell.type != CL.EXISTS:
                all_exist = False
                break
        if all_exist == True and self.settings['AEC'] == False:
            return False
        else:
            return True

    def CheckCE(self, row):
        compare_error = False
        for cell in row[1:]:
            if cell.type == CL.COMPERR:
                compare_error = True
                break
        if compare_error == True and self.settings['CEC'] == False:
            return False
        else:
            return True

    def CheckBL(self, label):
        if self.settings['BLC'] == False:
            return True
        else:
            return self.path_control(label,self.settings['BL'])

    def CheckWL(self, label):
        if self.settings['WLC'] == False:
            return True
        else:
            return not self.path_control(label,self.settings['WL'])
    
    def ShowRow(self, row):
        return self.CheckAE(row) and self.CheckCE(row) and self.CheckBL(row[0].label) and self.CheckWL(row[0].label)

    def toHTML(self):
        self.GetCurrentSettings()
        self.new_json = {}

        column = "minmax(150px,1fr) "
        result = f'<table style = "display: grid; grid-template-columns: {column*len(self.table[0])};">\n'
        result += self.RowToHTML(self.table[0], True)

        for row in self.table[1:]:
            result += self.RowToHTML(row, show = self.ShowRow(row))

        result += '\t</table>\n'

        return result

    def RowToHTML(self,row, head = False, show = True):
        margin = 2
        t = '\t'
        if (head):
            result = f'{t*margin}<thead>\n'
            margin += 1
        else:
            result = ''

        if show:
            result += f'{t*margin}<tr>\n'
        else:
            result += f'{t*margin}<tr hidden>\n'

        for cell in row:
            result += cell.toHTML(margin+1, head)
            self.new_json.update(cell.toJSON()) 

        result += f'{t*margin}</tr>\n'
        if (head):
            margin-=1
            result += f'{t*margin}</thead>\n'
        return result

    def GetCurrentSettings(self):
        self.settings = {}
        self.settings['WL'] = self.sPanel.white_list
        self.settings['BL'] = self.sPanel.black_list
        self.settings['WLC'] = self.sPanel.WL_check.GetValue()
        self.settings['BLC'] = self.sPanel.BL_check.GetValue()
        self.settings['AEC'] = self.sPanel.AE_check.GetValue()
        self.settings['CEC'] = self.sPanel.CE_check.GetValue()

class Cell():
    label = 'File path'
    type = CL.HEADER
    text = None
    uid = None

    def __init__(self, label = None, type = None, compare = None, file = None, uid = None) -> None:
        self.label = label  
        self.type = type
        self.file = file
        self.compare = compare
        self.uid = uid

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

    # def strip(self, str):
    #     if (str[-1] == '\n'):
    #         return str[:-1]

    def toJSON(self):
        if self.text == None:
            return {}
        return_dict = {self.uid : {"rows":[], "types":[]}}
        if type(self.text) == str:
            # self.text = self.strip(self.text)
            return_dict[self.uid]["rows"].append(self.text.replace('\t','&nbsp;&nbsp;&nbsp;&nbsp').replace('\n','<br>'))
            return_dict[self.uid]["types"].append(self.type)
        else:
            for line in self.text:
                if (line[:2] != '? '):
                    # line = self.strip(line)
                    return_dict[self.uid]["types"].append(CL.TYPES[line[:2]])
                    return_dict[self.uid]["rows"].append(line[2:].replace('\t','&nbsp;&nbsp;&nbsp;&nbsp').replace('\n','<br>'))
        return return_dict

    def toHTML(self,margin, head = False):
        t = '\t'
        if head:
            return f'{t*margin}<th data-type="text-long" id="{self.uid}" class = {self.type}>{self.label} <span class="resize-handle"></span> </th>\n'
        else:
            return f'{t*margin}<td id="{self.uid}" class = {self.type}>{self.label}</td>\n'