#! /usr/bin/env python

import sys, pprint, re, logging


logging.basicConfig(format='[%(levelname)s]: %(message)s')


class Parser:
    def __init__(self, instdict):
        self.comment = re.compile("^//.*")
        self.empty = re.compile("^\s*$")
        self.whitespace = re.compile("\s*")
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
                    parsedlines.append({"linum":linum, "type":instType, "inst":inst})
                except KeyError as ker:
                    logging.critical("Invalid instruction: %s on line %d in %s"%(ker,linum, filename))
                    exit()

        return parsedlines

if __name__=="__main__":
    parser=Parser()
    pprint.pprint(parser.parse(sys.argv[1]))
