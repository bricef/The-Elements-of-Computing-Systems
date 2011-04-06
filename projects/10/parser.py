#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET



#
# Strategy: create a parallel ET and add the right stuff as we iterate over the elements of the first one
#

if __name__ == "__main__":
    buf=[]
    for line in sys.stdin:
        buf.append(line)
        
    tokens = ET.fromstring("".join(buf) )
    parseTree = ET.Element("class")
    
    for token in tokens:
        print(token.tag, "->", token.text)
    
    
    
    print(ET.tostring(parseTree))
