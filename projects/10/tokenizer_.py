#! /usr/bin/env python

import sys, re, string
import xml.etree.ElementTree as ET

keywords = ["class","constructor","function",
            "method","field","static","var",
            "int","char","boolean","void","true",
            "false","null","this","let","do",
            "if", "else", "while", "return"]

symbols = "{}[]().,:;+-*/&|<>=~"



def isIn(kws):
    def isin(str):
        if str in kws:
            return True
        else:
            return False
    return isin
    
def matchRE(in_re):
    n_re = re.compile(in_re)
    def infunc(str):
        return n_re.match(str)
    return infunc


def isValidInt(str):
    isi = re.compile("[0-9]{1,5}")
    if isi.match(str):
        if -1 < int(str) < 32768:
            return True
        else:
            return False
    else:
        return False

bar = {
    'KEYWORD':isIn(keywords),
    'SYMBOL':isIn(symbols),
    'INTEGER_CONST':isValidInt,
    'STRING_CONST':matchRE(".*"),
    'IDENTIFIER':matchRE("[a-zA-Z_][a-zA-Z0-9_]*"),
}


states = [  "INSTRING",
            "IFR_KWD",
            "UNDEF",
            "INT",
            "COMMENT"
            ]


class Tokenizer:
    def __init__(self):
        self.tree = ET.Element("tokens")
        self.charbuffer = []
        self.state = "UNDEF"
    def push(self, char):
        ##
        # State UNDEF
        ##
        if self.state == "UNDEF":
            if char in "\"":
                #state beginstring
                self.charbuffer = []
                self.state = "INSTRING"
            elif char in symbols:
                temp = ET.SubElement(self.tree, "symbol")
                temp.text = char
                self.state = "UNDEF"
            elif char in string.digits:
                self.charbuffer = []
                self.charbuffer.append(char)
                self.state = "INT"
            elif char in string.whitespace:
                self.state = "UNDEF"
                self.charbuffer = []
            else:
                self.charbuffer = []
                self.charbuffer.append(char)
                self.state = "IFR_KWD"
        
        ##
        # State COMMENT
        ##
        elif self.state == "COMMENT":
                
        
        ##
        # State INSTRING
        ##
        elif self.state == "INSTRING":
            if char in '"':
                #we're ending string
                temp = ET.SubElement(self.tree, "StringConstant")
                temp.text = "".join(self.charbuffer)
                self.charbuffer = []
                self.state = "UNDEF"
            elif char in "\n":
                raise RuntimeError, "Newline in a literal string"
            else:
                self.charbuffer.append(char)
        ##
        # State IFR_KWD
        ##
        elif self.state == "IFR_KWD":
            if char in string.whitespace or char in symbols:
                tstr="".join(self.charbuffer)
                if tstr in keywords:
                    temp = ET.SubElement(self.tree, "keyword")
                    temp.text = "".join(self.charbuffer)
                    self.charbuffer=[]
                    self.state = "UNDEF"
                else:#we have an identifier
                    if self.charbuffer[0] in string.digits:
                        raise RuntimeError, "Invalid identifier."
                    else:
                        temp = ET.SubElement(self.tree, "identifier")
                        temp.text = "".join(self.charbuffer)
                        self.charbuffer =[]
                        self.state = "UNDEF"
            if char in symbols:
                temp = ET.SubElement(self.tree, "symbol")
                temp.text = char
                self.charbuffer = []
                self.state = "UNDEF"
            else:
                self.charbuffer.append(char)
                self.state = "IFR_KWD"
        
        ##
        # State INT
        ##
        elif self.state == "INT":
            if char in string.digits:
                self.charbuffer.append(char)
                self.state = "INT"
            if char in string.whitespace or char in symbols:
                if -1 < int("".join(self.charbuffer)) < 32768 :
                    temp = ET.SubElement(self.tree, "integerConstant")
                    temp.text = "".join(self.charbuffer)
                    self.charbuffer = []
                    self.state = "UNDEF"
                else:
                    raise RuntimeError, "Invalid Int range"
                if char in symbols:
                    temp = ET.SubElement(self.tree, "symbol")
                    temp.text = char
                    self.charbuffer = []
                    self.state = "UNDEF"
            else:
                raise RuntimeError, "Invalid Integer"
        
        
        #temp = ET.SubElement(self.tree, "char")
        #temp.text = char
    def xml(self):
        return ET.tostring(self.tree)
    def end(self):
        pass
        
    
if __name__ == "__main__":
    lc = 1
    tksr = Tokenizer()
    root = ET.Element("tokens")
    for line in sys.stdin:
        for char in line:
            try:
                tksr.push(char)
            except RuntimeError as err:
                print("Tokenisation error on line %d: %s"%(lc,str(err)))
                #sys.exit()
        lc = lc + 1
    tksr.end()
    print(tksr.xml())
            
