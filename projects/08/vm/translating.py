#
# Yes, this is verbose and ugly as hell. Screw you.
#




import common, pprint, re, logging

class Translator:
    def __init__(self):
        self.tc=0
        self.currentclass=""
        self.call_return=0
        self.transfn={
            "C_POP":        self.do_pop,
            "C_PUSH":       self.do_push,
            "C_ARITHMETIC": self.do_math,
            "C_LABEL":      self.do_label,
            "C_GOTO":       self.do_goto,
            "C_IFGOTO":     self.do_ifgoto,
            "C_FUNCTION":   self.do_funct,
            "C_CALL":       self.do_call,
            "C_RETURN":     self.do_return,
            }
        self.last_seen_fn=[]
    def newclass(self, clname):
        self.currentclass=clname
        self.last_seen_fn=[]
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
            ASM.append("@"+self.currentclass+"."+str(offset))
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
            ASM.append("@"+self.currentclass+"."+str(offset))
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

    def do_funct(self, inst=[]):
        self.last_seen_fn.append(inst[1])
        ASM=[]
        ASM.append("// DO_FUNC")
        nVars=int(inst[2])
        ASM.append("(%s)"%inst[1])
        for i in range(0, nVars):
            ASM.append(self.do_push(["push", "constant", "0"]))
            
        return "\n    ".join(common.flatten(ASM))
        
        
    def do_call(self, inst=[]):
        ASM=[]
        ASM.append("// DO_CALL: "+inst[1])
        self.call_return=self.call_return +1
        call_label="RETFROM_"+inst[1]+str(self.call_return)
        
        numargs= int(inst[2])
        # push return-address
        ASM.append("@%s"%(call_label))
        ASM.append("D=A")
        ASM.append("@SP")
        ASM.append("AM=M+1")
        ASM.append("A=A-1")
        ASM.append("M=D")
        # push LCL
        ASM.append("@LCL")
        ASM.append("D=M")
        ASM.append("@SP")
        ASM.append("AM=M+1")
        ASM.append("A=A-1")
        ASM.append("M=D")
        # push ARG
        ASM.append("@ARG")
        ASM.append("D=M")
        ASM.append("@SP")
        ASM.append("AM=M+1")
        ASM.append("A=A-1")
        ASM.append("M=D")
        # push THIS
        ASM.append("@THIS")
        ASM.append("D=M")
        ASM.append("@SP")
        ASM.append("AM=M+1")
        ASM.append("A=A-1")
        ASM.append("M=D")
        # push THAT
        ASM.append("@THAT")
        ASM.append("D=M")
        ASM.append("@SP")
        ASM.append("AM=M+1")
        ASM.append("A=A-1")
        ASM.append("M=D")
        # ARG = SP-n-5
        ASM.append("@SP")
        ASM.append("D=M")
        ASM.append("@"+str(numargs+5))#we're doing work in machine that could be done in-compiler: numargs+5
        ASM.append("D=D-A")
        ASM.append("@ARG")
        ASM.append("M=D")
        # LCL = SP
        ASM.append("@SP")
        ASM.append("D=M")
        ASM.append("@LCL")
        ASM.append("M=D")
        # goto f
        ASM.append("@%s"%(str(inst[1])))
        ASM.append("0;JMP")
        # set label return-address
        ASM.append("(%s)"%(call_label))
        
        return "\n    ".join(common.flatten(ASM))
        
    def do_return(self, inst=[]):
        #if self.last_seen_fn:
        #    self.last_seen_fn.pop()
        ASM=[]
        ASM.append("// DO_RETURN")
        #FRAME=LCL
        ASM.append("@LCL")
        ASM.append("D=M")
        ASM.append("@13") #FRAME in M[13]
        ASM.append("M=D")
        # RET = *(FRAME-5)
        ASM.append("@5")
        ASM.append("A=D-A")
        ASM.append("D=M")
        ASM.append("@14") #RET in M[14]
        ASM.append("M=D")
        # *ARG = pop()
        ASM.append("@SP")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@ARG")
        ASM.append("A=M")
        ASM.append("M=D")
        # SP = ARG +1
        ASM.append("@ARG")
        ASM.append("D=M+1")
        ASM.append("@SP")
        ASM.append("M=D")
        # THAT = *(FRAME-1)
        ASM.append("@13")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@THAT")
        ASM.append("M=D")
        # THIS = *(FRAME-2)
        ASM.append("@13")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@THIS")
        ASM.append("M=D")
        # ARG = *(FRAME-3)
        ASM.append("@13")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@ARG")
        ASM.append("M=D")
        # LCL = *(FRAME-4)
        ASM.append("@13")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@LCL")
        ASM.append("M=D")
        # goto RET
        ASM.append("@14")
        ASM.append("A=M")
        ASM.append("0;JMP")
        return "\n    ".join(common.flatten(ASM))
        
    def do_goto(self, inst=[]):
        ASM=[]
        label=inst[1]
        if self.last_seen_fn:
            label=self.last_seen_fn[-1]+"$"+label
        ASM.append("@%s"%(label))
        ASM.append("0;JMP")
        return ASM
    def do_label(self, inst=[], prefix=""):
        ASM=[]
        label=inst[1]
        if self.last_seen_fn:
            label=self.last_seen_fn[-1]+"$"+label
        ASM.append("(%s)"%(label))
        return ASM
    def do_ifgoto(self, inst=[]):
        ASM=[]
        label=inst[1]
        if self.last_seen_fn:
            label=self.last_seen_fn[-1]+"$"+label
        ASM.append("@SP")
        ASM.append("AM=M-1")
        ASM.append("D=M")
        ASM.append("@%s"%(label))
        ASM.append("D;JNE")
        
        return ASM
    def translate(self, parsedlines):
        asmlines=[]
        #initialise the stack pointer
        asmlines.append("@256")
        asmlines.append("D=A")
        asmlines.append("@SP")
        asmlines.append("M=D")
        #Call Sys.init
        asmlines.append(self.do_call(["call", "Sys.init", 0]))
        
        for line in parsedlines:
            asmlines.append(self.transfn[line["type"]](line["inst"]))
        return common.flatten(asmlines)

