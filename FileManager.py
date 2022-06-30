import os
import difflib as df
import ConstantLib as CL
from debug import timer

#@timer
def GetFiles(dir): #Returned all files from argument directory
    dir = dir.replace('\\','/')
    tree = os.walk(dir)
    files = []
    for leaf in tree:
        for file_name in leaf[2]:
            file_path = leaf[0].replace(dir,'').replace('\\','/')+'/'
            file = file_path+file_name
            files.append(file)
    return dir,files

#@timer
def ConcatLists(lists):  #Concatination lists with only original values
    result_list = []
    for lst in lists:
        for el in lst:
            if el not in result_list:
                result_list.append(el)
    result_list.sort()
    return result_list

#@timer
def GetText(file_path, one_line = False): #returned text from file
    text = []
    with open(file_path, 'r', encoding='utf-8') as file:
        if one_line:
            text = file.read()
        else:
            text = file.readlines()

    return text

#@timer
def isDifferens(file_1, file_2): #returned false, if input files are similar
    text_1 = GetText(file_1)
    text_2 = GetText(file_2)
    return (text_1 != text_2)

#@timer
def isCanOpen(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.readline()
    
#@timer
def GetDifferens(file_1,file_2): #returned compare for 2 files
    text_1 = GetText(file_1)
    text_2 = GetText(file_2)
    result_list = []
    for line in df.ndiff(text_1,text_2):
        if line[:2] != '? ':
            result_list.append(line)
    return result_list
    # return list(df.ndiff(text_1,text_2))
    # result_list = []
    # add_flag = False
    # for line in df.ndiff(text_1,text_2):
    #     if line[:2] == '  ':
    #         if add_flag:
    #             result_list[-1] = result_list[-1]+line
    #         else:
    #             result_list.append(line)
    #             add_flag = True
    #     elif line[:2] == '- ' or line[:2] == '+ ':
    #         result_list.append(line)
    #         add_flag = False

#@timer
def CompareFiles(file_1,file_2): #returned files state
    file_1_isExist = os.path.exists(file_1)
    file_2_isExist = os.path.exists(file_2)
    if file_1_isExist:
        about_1 = CL.EXISTS
    else:
        about_1 = CL.MISSING
    if file_2_isExist:
        about_2 = CL.EXISTS
    else:
        about_2 = CL.MISSING

    try:
        if (file_1_isExist):
            isCanOpen(file_1)
            if (file_2_isExist):
                if (isDifferens(file_1,file_2)):
                    about_2 = CL.DIFFERS
            else:
                about_2 = CL.MISSING
        else:
            if (file_2_isExist):
                isCanOpen(file_2)
                about_2 = CL.DIFFERS
            else:
                about_2 = CL.MISSING
    except:
        about_1 = CL.COMPERR
        about_2 = CL.COMPERR

    return about_1, about_2

# GetFiles(r"D:\GIT\Comparator-v.2.0\test_area")
# ConcatLists([['123','asd','fr23'],['123','asd','far23'],['1234','asd','fr23']])
