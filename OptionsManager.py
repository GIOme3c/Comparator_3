def getFileDec(func):
    def wrapper():
        with open(".default","r") as file:
            return func(file.readlines())
    return wrapper

@getFileDec
def getProjects(text):
    pass

@getFileDec
def getCompares(text):
    pass

@getFileDec
def getHeaders(text):
    pass

@getFileDec
def getWL(text):
    pass

@getFileDec
def getBL(text):
    pass

@getFileDec
def getWLC(text):
    pass

@getFileDec
def getBLC(text):
    pass

@getFileDec
def getAEC(text):
    pass

@getFileDec
def getCEC(text):
    pass


def saveOptions(projects = None, compares = None, headers = None, 
                WL = None, BL = None, WLC = None, BLS = None,
                AEC = None, CEC = None):
    pass