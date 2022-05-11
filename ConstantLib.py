import wx,os

CUR_PATH = os.getcwd()
BASE_URL = f'file:{CUR_PATH}/content/content.html'

FONT_10 = wx.Font()
FONT_10.SetPointSize(10)

# SEPARATOR = "%/0/%"
HEADER = 'header'
FNAME = 'file_name'
EXISTS = 'exists'
DIFFERS = 'differs'
MISSING = 'missing'
COMPERR = 'compare_error'
EMPTY = 'empty'
# DEFAULT = 'default'

COLOUR = {
    HEADER:wx.Colour(204,204,255),
#     FNAME:wx.Colour(204,255,255),
#     EXISTS:wx.Colour(153,255,204),
#     DIFFERS:wx.Colour(255,255,204),
#     MISSING:wx.Colour(204,153,204),
#     COMPERR:wx.Colour(255,0,0),
#     EMPTY:wx.Colour(153,153,153),
#     DEFAULT:wx.Colour(255,255,255)
}

# DBG = COLOUR[DEFAULT]

# TCOLOUR = {
#     EXISTS:wx.Colour(193,255,224),
#     DIFFERS:wx.Colour(193,255,224),
#     MISSING:wx.Colour(255,204,204),
#     COMPERR:wx.Colour(153,255,204),
#     EMPTY:wx.Colour(153,255,204),
#     DEFAULT:wx.Colour(0,0,0),
#     '  ':wx.Colour(255,255,255),
#     '- ':wx.Colour(255,204,204),
#     '+ ':wx.Colour(193,255,224),
# }

def HSIZE():
    return wx.GetDisplaySize()[0]
def VSIZE():
    return wx.GetDisplaySize()[1]
