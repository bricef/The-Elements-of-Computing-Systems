#! /usr/bin/env python

import sys
from tools import *
import refs

orig=[]
compiled=[]
pretty_compiled=[]

def firstpass(lines, symbols):
    instcounter=0
    for line, linum in zip(lines, range(0, len(lines))):
        splitline = re.split(commentmarker, line)
        if whitespace.match( splitline[0]):
            pass
        else: #we have a line
            cleanline = splitline[0].strip()
            try:
                if label.match(cleanline):
                    symbols[cleanline[1:-1]]=instcounter
                elif address.match(cleanline):
                    instcounter = instcounter+1
                elif cinst.match(cleanline):
                    instcounter = instcounter+1
                else:
                   raise RuntimeError, "Invalid Syntax" 
                    
            except (RuntimeError, ValueError) as ex:
                print "Error on line %d:"%(linum+1), ex
                exit()
    return symbols

def assemble(lines, symbols, variables):
    for line, linum in zip(lines, range(0, len(lines))):
        #filter out comments
        splitline = re.split(commentmarker, line)
        if whitespace.match( splitline[0]):
            pass
        else: #we have a line
            cleanline = splitline[0].strip()
            try:
                if label.match(cleanline):
                    orig.append(cleanline)
                    pretty_compiled.append("")
                elif address.match(cleanline):
                    orig.append(cleanline.ljust(16))
                    compline, symbols, variables = HandleA(cleanline, symbols, variables)
                    compiled.append(compline)
                    pretty_compiled.append(compline)
                                    
                elif cinst.match(cleanline):
                    orig.append(cleanline.ljust(16))
                    pretty_compiled.append(HandleC(cleanline))
                    compiled.append(HandleC(cleanline))
                else:
                   raise RuntimeError, "Invalid Syntax" 
                    
            except (RuntimeError, ValueError) as ex:
                print "Error on line %d:"%(linum+1), ex
                exit()


if __name__=="__main__":
    infile=open(sys.argv[1], "r").readlines()
    symbols = refs.symboltable
    symbols = firstpass(infile, symbols)
    variables = refs.variables
    assemble(infile, symbols, variables)
    
    if len(sys.argv) == 2 :
        for inst, bin in zip(orig, pretty_compiled):
            print inst, bin
    else:
        outf = open(sys.argv[2], "w")
        outf.write("\n".join(compiled))
        outf.write("\n")
        outf.close()
