def getOption(start = None, end = None):
    
    start_pos = 0
    end_pos = None
    
    with open(".default","r") as file:
        text = file.readlines()
        for i in range(len(text)):
            if text[i].startswith(start):
                start_pos = i
                break
        if (end is not None):
            for i in range(start_pos+1,len(text),1):
                if text[i].startswith(end):
                    end_pos = i
                    break
            return text[start_pos+1:end_pos]
        else:
            return bool(text[start_pos][-1])


def getOptions():
    options = {}
    options['projects'] = {string.split(' ')[0]: string.split(' ')[1] for string in getOption("$projects","$endproject")}
    options['compares'] = [(string.split(' ')) for string in getOption("$compares","$endcompares")]
    options['headers'] = [(string.split(' ')) for string in getOption("$headers","$endheaders")]
    options['WL'] = [string for string in getOption("$WL","$endWL")]
    options['BL'] = [string for string in getOption("$BL","$endBL")]
    options['WLC'] = getOption('$WLC')
    options['BLC'] = getOption('$BLC')
    options['AEC'] = getOption('$AEC')
    options['CEC'] = getOption('$CEC')

    return options


def saveOptions(projects = None, compares = None, headers = None, 
                WL = None, BL = None, WLC = None, BLS = None,
                AEC = None, CEC = None):
    pass