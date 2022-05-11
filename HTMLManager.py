import os

def END():
    if os.path.exists('content/content.html'):
        os.remove('content/content.html')

def getTemplate():
    with open('content/template.html', 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def rewriteContentPage(newPage):
    if os.path.exists('content/content.html'):
        os.remove('content/content.html')
    with open('content/content.html', 'x', encoding='utf-8') as file:
        file.write(newPage)

def setStartPage():
    setContentPage('<h1>Compare some projects</h1>')

def setContentPage(content):
    cPage = TEMPLATE_PAGE.replace('###CONTENT###',content)
    rewriteContentPage(cPage)

def setLoadPage():
    pass

def getResult():
    pass

TEMPLATE_PAGE = getTemplate()