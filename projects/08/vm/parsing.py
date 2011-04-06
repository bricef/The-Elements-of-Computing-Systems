#! /usr/bin/env python

import sys, pprint, re, logging


logging.basicConfig(format='[%(levelname)s]: %(message)s')


class Parser:
    def __init__(self, instdict):
        self.comment = re.compile("^//.*")
        self.empty = re.compile("^\s*$")
        self.whitespace = re.compile("\s*")
        self.validlabel=re.compile("^[a-zA-Z_:.][a-zA-Z0-9_:.]+$")
        
        self.instdict=instdict

    def parse(self, filename):
        f=open(filename, "r")
        parsedlines=[]
        
        rawlines=f.readlines()
        f.close()

        for line, linum in zip(rawlines, range(0, len(rawlines))):
            line=line.split("//")[0]
            if self.comment.match(line.strip()) or self.empty.match(line.strip()):
                pass
            else:
                inst = re.split(self.whitespace, line.strip())
                try:
                    instType = self.instdict[inst[0]]
                    if len(inst) > 1 and inst[1] in ["label", "goto", "if-goto", "function", "call"]:
                        assert self.validlabel.match(inst[1])
                    parsedlines.append({"linum":linum, "type":instType, "inst":inst})
                except KeyError as ker:
                    logging.critical("Invalid instruction: %s on line %d in %s"%(ker,linum, filename))
                    exit()
                except AssertionError as ase:
                    logging.critical("Invalid label on line %d in %s "%(linum, filename))
                    exit()

        return parsedlines

if __name__=="__main__":
    parser=Parser()
    pprint.pprint(parser.parse(sys.argv[1]))
