#! /usr/bin/env python

from refs import *

def int2bin(n, count=16):
        return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


def HandleA(inst, symbols, variables):
    inst = inst.strip("@")
    value=None
    if isnummer.match(inst):
        value = int(inst)
        if value < 0:
            raise RuntimeError, "constant values cannot be less than 0"
    elif symbol.match(inst):
        if variables.has_key(inst):
            value=variables[inst]
        elif symbols.has_key(inst):
            value=symbols[inst]
        else:
            maxvar=max(variables.values())
            if maxvar<16:
                maxvar=16
            else:
                maxvar=maxvar+1
            variables[inst]=maxvar
            value=maxvar
    else:
        raise RuntimeError, "Invalid instruction"
    
    return int2bin(value), symbols, variables

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
