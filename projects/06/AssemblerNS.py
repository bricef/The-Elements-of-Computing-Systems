#! /usr/bin/env python

import sys
import re

commentmarker = re.compile("//")
whitespace = re.compile("^\s*$")
address = re.compile("^@")
cinst = re.compile(".*[=|;].*")
isnummer = re.compile("^[0-9]*$")


symboltable={
        "SP":0,
        "LCL":1,
        "ARG":2,
        "THIS":3,
        "THAT":4,
        "SCREEN":16384,
        "ENDSCREEN":24575,
        "KBD":24576,
        "R0":0, "R1":1, "R2":2, "R3":3, "R4":4, "R5":5, "R6":6, "R7":7, "R8":8, "R9":9, "R10":10, "R11":11, "R12":12, "R13":13, "R14":14, "R15":15,
        }

jumpdict={
        None:"000",
        "JGT":"001",
        "JEQ":"010",
        "JGE":"011",
        "JLT":"100",
        "JNE":"101",
        "JLE":"110",
        "JMP":"111"
        }

destdict={
        None:"000",
        "M":"001",
        "D":"010",
        "MD":"011",
        "A":"100",
        "AM":"101",
        "AD":"110",
        "AMD":"111"
        }
        
compdict={
        "0":    "0101010",
        "1":    "0111111",
        "-1":   "0111010",
        "D":    "0001100",
        "A":    "0110000",
        "!D":   "0001101",
        "!A":   "0110001",
        "D+1":  "0011111",
        "A+1":  "0110111",
        "D-1":  "0001110",
        "A-1":  "0110010",
        "D+A":  "0000010",
        "D-A":  "0010011",
        "A-D":  "0000111",
        "D&A":  "0000000",
        "D|A":  "0010101",
        "M":    "1110000",
        "!M":   "1110001",
        "-M":   "1110011",
        "M+1":  "1110111",
        "M-1":  "1110010",
        "D+M":  "1000010",
        "D-M":  "1010011",
        "M-D":  "1000111",
        "D&M":  "1000000",
        "D|M":  "1010101",
    }




instructions=[]
orig=[]
compiled=[]
def int2bin(n, count=16):
        return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


def HandleA(inst):
    inst = inst.strip("@")
    value=None
    if isnummer.match(inst):
        value = int(inst)
        if value < 0:
            raise RuntimeError, "constant values cannot be less than 0"
    else:
        raise RuntimeError, "Invalid instruction"
    
    return int2bin(value)

def HandleC(inst):
    
    DEST=None
    COMP=None
    JUMP=None
    
    splitjmp = inst.split(";")
    if len(splitjmp) == 2: #we have a jump!
        JUMP=splitjmp[-1]
    elif len(splitjmp) > 2:
        raise RuntimeError, "Invalid instruction"
    splitdest = splitjmp[0].split("=")
    if len(splitdest) == 2: #we have dest!
        DEST=splitdest[0]
        COMP=splitdest[1]
    elif len(splitdest) == 1:
        COMP=splitdest[0]
    else:
        raise RuntimeError, "Invalid instruction"
    try:
        compiled_inst=["111", compdict[COMP],destdict[DEST],jumpdict[JUMP]]
    except KeyError as ex:
        raise RuntimeError, "Unrecognised instruction: "+str(ex)
        
        
    return "".join(compiled_inst)

def Assemble(lines):
    for line, linum in zip(lines, range(0, len(lines))):
        #filter out comments
        splitline = re.split(commentmarker, line)
        if whitespace.match( splitline[0]):
            pass
        else: #we have a line
            cleanline = splitline[0].strip()
            instructions.append(cleanline)
            try:
                if address.match(cleanline):
                    orig.append(cleanline.ljust(16))
                    compiled.append(HandleA(cleanline))
                                    
                elif cinst.match(cleanline):
                    orig.append(cleanline.ljust(16))
                    compiled.append(HandleC(cleanline))
                    
            except (RuntimeError, ValueError) as ex:
                print "Error on line %d:"%(linum+1), ex
                exit()


if __name__=="__main__":
    filename=sys.argv[1]
    Assemble(open(filename, "r").readlines())
    if len(sys.argv) == 2 :
        for inst, bin in zip(orig, compiled):
            print inst, bin
    else:
        outf = open(sys.argv[2], "w")
        outf.write("\n".join(compiled))
        outf.write("\n")
        outf.close()
