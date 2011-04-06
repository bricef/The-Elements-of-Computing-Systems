#! /usr/bin/env python

import sys, re, string



keywords = ["class","constructor","function",
            "method","field","static","var",
            "int","char","boolean","void","true",
            "false","null","this","let","do",
            "if", "else", "while", "return"]

CHARBUFFER = []
CSTATE = "UDEF"
CURRENTCHAR = ""


def A():#append char to charbuffer
    global CHARBUFFER
    CHARBUFFER.append(CURRENTCHAR)
    
def C():#clear charbuffer
    global CHARBUFFER
    CHARBUFFER = []
    
def ms():#make symbol
    # temp = ET.SubElement(TKNTREE, "symbol")
    # temp.text = CURRENTCHAR
    print("<symbol>%s</symbol>"%(CURRENTCHAR))

def meolc():
    pass
    
def mmlc():
    pass
    
def mks():
    #temp = ET.SubElement(TKNTREE, "StringConstant")
    #temp.text = "".join(CHARBUFFER)
    print("<StringConstant>%s</StringConstant>"%("".join(CHARBUFFER)))
    
def mi():
    tempint = int("".join(CHARBUFFER))
    if -1 < tempint < 32768:
        #valid int
        print("<integerConstant>%d</integerConstant>"%(tempint))
    else:
        raise RuntimeError("Invalid int range")
    
def miok():
    text = "".join(CHARBUFFER)
    if text in keywords:
        print("<keyword>%s</keyword>"%(text))
    else:
        print("<identifier>%s</identifier>"%(text))
    

def ERROR():
    raise RuntimeError("err")

state_table = {
"UDEF" : {
    string.digits           : [A, "INT"],
    "{}[]().,:;+-&|<>=~"    : [A, ms, "UDEF", C],
    "/"                     : [A, "ICOM?"],
    string.whitespace       : [C, "UDEF"],
    string.ascii_letters    : [A, "IFR_KWD"],
    "*"                     : [A, "IFR_KWD"],
    "\""                    : [C, "STR"],
    },
    
"EOLCOM" : {
    string.digits           : [A, "EOLCOM"],
    "{}[]().,:;+-&|<>=~"    : [A, "EOLCOM"],
    "/"                     : [A, "EOLCOM"],
    "\t\x0b\x0c\r"          : [A, "EOLCOM"],
    "\n"                    : [meolc, C, "UDEF"],
    string.ascii_letters    : [A, "EOLCOM"],
    "*"                     : [A, "EOLCOM"],
    "\""                    : [A, "EOLCOM"],
    },
"MLCOM" : {
    string.digits           : [A, "MLCOM"],
    "{}[]().,:;+-&|<>=~"    : [A, "MLCOM"],
    "/"                     : [A, "MLCOM"],
    string.whitespace       : [A, "MLCOM"],
    string.ascii_letters    : [A, "MLCOM"],
    "*"                     : [A, "ECOM?"],
    "\""                    : [A, "MLCOM"],
    },
"STR" : {
    string.digits           : [A, "STR"],
    "{}[]().,:;+-&|<>=~"    : [A, "STR"],
    "/"                     : [A, "STR"],
    "\t\x0b\x0c\r"          : [A, "STR"],
    "\n"                    : [ERROR],
    string.ascii_letters    : [A, "STR"],
    "*"                     : [A, "STR"],
    "\""                    : [mks, C, "UDEF"],
    },
"INT" : {
    string.digits           : [A, "INT"],
    "{}[]().,:;+-&|<>=~"    : [mi, C, A, ms, C, "UDEF"],
    "/"                     : [mi, C, A, "ICOM?"],
    "\t\x0b\x0c\r"          : [mi, C, "UDEF"],
    "\n"                    : [mi, C, "UDEF"],
    string.ascii_letters    : [ERROR],
    "*"                     : [mi, C, A, ms, C, "UDEF"],
    "\""                    : [ERROR],
    },
"ICOM?" : {
    string.digits           : [ms, C, A, "INT"],
    "{}[]().,:;+-&|<>=~"    : [ms, C, A, ms, C, "UDEF"],
    "/"                     : ["EOLCOM"],
    "\t\x0b\x0c\r"          : [ms, C, "UDEF"],
    "\n"                    : [ms, C, "UDEF"],
    string.ascii_letters    : [ms, C, A, "IFR_KWD"],
    "*"                     : [C, "MLCOM"],
    "\""                    : [ERROR],
    },
"ECOM?" : {
    string.digits           : [A, "MLCOM"],
    "{}[]().,:;+-&|<>=~"    : [A, "MLCOM"],
    "/"                     : [mmlc, C, "UDEF"],
    string.whitespace       : [A, "MLCOM"],
    string.ascii_letters    : [A, "MLCOM"],
    "*"                     : [A, "MLCOM"],
    "\""                    : [A, "MLCOM"],
    },
"IFR_KWD" : {
    string.digits           : [A, "IFR_KWD"],
    "{}[]().,:;+-&|<>=~"    : [miok, C, A, ms, C, "UDEF"],
    "/"                     : [miok, C, A, "ICOM?"],
    string.whitespace       : [miok, C, "UDEF"],
    string.ascii_letters    : [A, "IFR_KWD"],
    "*"                     : [miok, C, A, ms, C, "UDEF"],
    "\""                    : [miok, C, "STR"],
    },
}


        
def pushchar(char):
    CURRENTCHAR = char
    global CSTATE
    #print CSTATE
    for key in list(state_table[CSTATE].keys()):
        if char in key:
            for action in state_table[CSTATE][key]:
                if isinstance(action, str):
                    CSTATE = action
                else:
                    action()
            break
    
    
if __name__ == "__main__":
    print("<tokens>")
    lc = 1
    for line in sys.stdin:
        for char in line:
            CURRENTCHAR=char
            try:
                pushchar(char)
            except RuntimeError as err:
                print(("Tokenisation error on line %d: %s"%(lc,str(err))))
                #sys.exit()
        lc = lc + 1
    print("</tokens>")
            
