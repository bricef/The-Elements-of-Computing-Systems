#! /usr/bin/env python

import sys, os, pprint

from translating import Translator
from parsing import Parser
import common



instdict = {
    "push":     "C_PUSH",
    "pop":      "C_POP",
    #"label":    "C_LABEL",
    #"goto":     "C_GOTO",
    #"if-goto":  "C_IFGOTO",
    #"function": "C_FUNCTION",
    #"call":     "C_CALL",
    #"return":   "C_RETURN",
    "add":      "C_ARITHMETIC",
    "sub":      "C_ARITHMETIC",
    "neg":      "C_ARITHMETIC",
    "eq":       "C_ARITHMETIC",
    "gt":       "C_ARITHMETIC",
    "lt":       "C_ARITHMETIC",
    "and":      "C_ARITHMETIC",
    "or":       "C_ARITHMETIC",
    "not":      "C_ARITHMETIC",
    }



def usage():
    print"""
python S1VM.py <source>
    where <source> is a valid vm file or a folder containing vm files.
"""
if __name__=="__main__":
    translator=Translator()
    parser=Parser(instdict)
    
    outASM=[]
    
    try:
        givenpath = sys.argv[1]
    except IndexError:
        usage()
        exit()

    if os.path.isdir(givenpath):
        for file in os.listdir(givenpath):
            if file[-3:] == ".vm":
                outASM.append(translator.translate(parser.parse(os.path.join(givenpath, file))))
    elif os.path.isfile(givenpath) and givenpath[-3:] == ".vm":
            outASM.append(translator.translate(parser.parse(givenpath)))
    else:
        print("Error: Path supplied is invalid!")
        exit()

    print "\n".join(common.flatten(outASM))
