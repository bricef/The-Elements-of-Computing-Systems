
import common, pprint

class Translator:
    def __init__(self):
        self.tc=0
        self.transfn={
            "C_POP":        self.do_pop,
            "C_PUSH":       self.do_push,
            "C_ARITHMETIC": self.do_math,
            }
        self.segvals={
            "static":16,#fixed
            "pointer":3,#fixed
            "temp":5,#fixed
            "this":0,
            "that":0,
            "argument":0,
            "local":0,
            }
    def segval(self, segment):
        pass

    def do_pop(self, inst=[]):
        #print " ".join(inst)
        ASM=[]
        destAddress=None
        segment = inst[1]
        offset = int(inst[2])
        
        
        if segment == "constant":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M") #D is now y
            ASM.append("@"+str(offset))
            ASM.append("M=D")
        elif segment == "this":
            ASM.append("@THIS")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("D=D+A")   # D now has target address
            ASM.append("@13")
            ASM.append("M=D")
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@13")
            ASM.append("A=M")
            ASM.append("M=D")
        elif segment == "that":
            ASM.append("@THAT")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("D=D+A")   # D now has target address
            ASM.append("@13")
            ASM.append("M=D")
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@13")
            ASM.append("A=M")
            ASM.append("M=D")
        elif segment == "pointer":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@"+str(offset+3))
            ASM.append("M=D")
        elif segment == "temp":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@"+str(offset+5))
            ASM.append("M=D")
        elif segment == "argument":
            ASM.append("@ARG")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("D=D+A")   # D now has target address
            ASM.append("@13")
            ASM.append("M=D")
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@13")
            ASM.append("A=M")
            ASM.append("M=D")
        elif segment == "local":
            ASM.append("@LCL")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("D=D+A")   # D now has target address
            ASM.append("@13")
            ASM.append("M=D")
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@13")
            ASM.append("A=M")
            ASM.append("M=D")
        elif segment == "static":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@"+str(offset+16))
            ASM.append("M=D")
        #print "  -> ", ASM
        return ASM
    def do_push(self, inst=[]):
        #print " ".join(inst)
        ASM=[]
        pushedValue=None
        segment = inst[1]
        offset = int(inst[2])
        if segment == "constant":
            ASM.append("@"+str(offset))
            ASM.append("D=A")
        elif segment == "this":
            ASM.append("@THIS")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("A=D+A")
            ASM.append("D=M")
        elif segment == "that":
            ASM.append("@THAT")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("A=D+A")
            ASM.append("D=M")
        elif segment == "pointer":
            ASM.append("@"+str(3+offset))
            ASM.append("D=M")
        elif segment == "temp":
            ASM.append("@"+str(offset+5))
            ASM.append("D=M")
        elif segment == "argument":
            ASM.append("@ARG")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("A=D+A")
            ASM.append("D=M")
        elif segment == "local":
            ASM.append("@LCL")
            ASM.append("D=M")
            ASM.append("@"+str(offset))
            ASM.append("A=D+A")
            ASM.append("D=M")
        elif segment == "static":
            ASM.append("@"+str(offset+16))
            ASM.append("D=M")
        ASM.append("@SP")
        ASM.append("A=M")
        ASM.append("M=D")
        ASM.append("@SP")
        ASM.append("M=M+1")
        #this should use an external syntax file and templates for @A, DEST, COMP, JUMP 
        #simple string templates would work great too.
        
        #print "  -> ", ASM
        return ASM

    def do_math(self, inst=[]):
        #print " ".join(inst)
        ASM=[]
        #A translation table would be nicer
        if inst[0] == "add":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=D+M")
        elif inst[0] == "sub":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=M-D")
        elif inst[0] == "neg":
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=-M")
        elif inst[0] == "eq":
            ASM.append("@SP")
            ASM.append("AM=M-1") #stackpointer down, address down
            ASM.append("D=M") #D contains y
            ASM.append("@SP")
            ASM.append("A=M-1") #address to x
            ASM.append("D=M-D") #D=x-y
            
            ASM.append("M=-1") #set true
            ASM.append("@TRUE"+str(self.tc))
            ASM.append("D;JEQ")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=0")
            ASM.append("(TRUE"+str(self.tc)+")")
            self.tc=self.tc+1
            #TODO
        elif inst[0] == "gt":
            ASM.append("@SP")
            ASM.append("AM=M-1") #stackpointer down, address down
            ASM.append("D=M") #D contains y
            ASM.append("@SP")
            ASM.append("A=M-1") #address to x
            ASM.append("D=M-D") #D=x-y
            
            ASM.append("M=-1") #set true
            ASM.append("@TRUE"+str(self.tc))
            ASM.append("D;JGT")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=0")
            ASM.append("(TRUE"+str(self.tc)+")")
            self.tc=self.tc+1
            #TODO
            pass
        elif inst[0] == "lt":
            ASM.append("@SP")
            ASM.append("AM=M-1") #stackpointer down, address down
            ASM.append("D=M") #D contains y
            ASM.append("@SP")
            ASM.append("A=M-1") #address to x
            ASM.append("D=M-D") #D=x-y
            
            ASM.append("M=-1") #set true
            ASM.append("@TRUE"+str(self.tc))
            ASM.append("D;JLT")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=0")
            ASM.append("(TRUE"+str(self.tc)+")")
            self.tc=self.tc+1
            #TODO
            pass
        elif inst[0] == "and":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=D&M")
        elif inst[0] == "or":
            ASM.append("@SP")
            ASM.append("AM=M-1")
            ASM.append("D=M")
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=D|M")
        elif inst[0] == "not":
            ASM.append("@SP")
            ASM.append("A=M-1")
            ASM.append("M=!M")
        
        return ASM

    def translate(self, parsedlines):
        asmlines=[]
        for line in parsedlines:
            asmlines.append(self.transfn[line["type"]](line["inst"]))
        return common.flatten(asmlines)

