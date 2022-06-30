import os, json
from debug import timer


#@timer
def END():
    if os.path.exists('content/content.html'):
        os.remove('content/content.html')
    if os.path.exists('content/data.json'):
        os.remove('content/data.json')

#@timer
def getTemplate():
    with open('content/template.html', 'r', encoding='utf-8') as file:
        text = file.read()
    return text

#@timer
def rewriteContentPage(newPage):
    content_path = 'content/content.html'
    if os.path.exists(content_path):
        os.remove(content_path)
    with open(content_path, 'x', encoding='utf-8') as file:
        file.write(newPage)

#@timer
def setData(newJSON):
    data_path = 'content/data.json'
    if os.path.exists(data_path):
        os.remove(data_path)
    with open(data_path, 'x', encoding='utf-8') as file:
        file.write('json = '+json.dumps(newJSON,separators=(',', ':')))

#@timer
def setStartPage():
    setContentPage('<h1>Compare some projects</h1>')

#@timer
def setContentPage(content):
    cPage = TEMPLATE_PAGE.replace('###CONTENT###',content)
    rewriteContentPage(cPage)

#@timer
def setLoadPage():
    pass

#@timer
def getResult():
    pass

TEMPLATE_PAGE = getTemplate()