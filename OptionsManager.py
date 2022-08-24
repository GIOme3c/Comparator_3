from Content import HeaderRow

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
            return int(text[start_pos].rstrip()[-1])


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

def transform_value(value):
    if type(value) == list:
        if (value and type(value[0]) != HeaderRow()):
            result = [x+"\n" for x in value]
        else:
            result = [x.get_save_data() for x in value] 
    if type(value) == dict:
        result = [str(x)+" "+str(value[x])+"\n" for x in value]
    if type(value) == type(False):
        return int(value)
    else:
        return result

def saveOption(start = None, end = None, value = None):
    value = transform_value(value)

    with open(".default","r") as file:
        text = file.readlines()

    with open(".default","w") as file:
        for i in range(len(text)):
            if text[i].startswith(start):
                start_pos = i
                break
        if (end is not None):
            for i in range(start_pos+1,len(text),1):
                if text[i].startswith(end):
                    end_pos = i
                    break
            file.writelines(text[:start_pos+1]+value+text[end_pos:])
        else:
            text[start_pos] = start+f" : {value}\n"
            file.writelines(text)

def saveOptions(projects = None, compares = None, headers = None, 
                WL = None, BL = None, WLC = None, BLS = None,
                AEC = None, CEC = None):
    saveOption("$projects","$endproject",projects)
    saveOption("$compares","$endcompares",compares)
    saveOption("$headers","$endheaders",headers)
    saveOption("$WL","$endWL",WL)
    saveOption("$BL","$endBL",BL)
    saveOption("$WLC",None,WLC)
    saveOption("$BLC",None,BLS)
    saveOption("$AEC",None,AEC)
    saveOption("$CEC",None,CEC)