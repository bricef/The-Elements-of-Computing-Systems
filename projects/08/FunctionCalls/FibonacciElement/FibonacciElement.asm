@256
D=A
@SP
M=D
// DO_CALL: Sys.init
    @RETFROM_Sys.init1
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @5
    D=D-A
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @Sys.init
    0;JMP
    (RETFROM_Sys.init1)
// DO_FUNC
    (Main.fibonacci)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
D=M-D
M=-1
@TRUE0
D;JLT
@SP
A=M-1
M=0
(TRUE0)
@SP
AM=M-1
D=M
@Main.fibonacci$IF_TRUE
D;JNE
@Main.fibonacci$IF_FALSE
0;JMP
(Main.fibonacci$IF_TRUE)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// DO_RETURN
    @LCL
    D=M
    @13
    M=D
    @5
    A=D-A
    D=M
    @14
    M=D
    @SP
    AM=M-1
    D=M
    @ARG
    A=M
    M=D
    @ARG
    D=M+1
    @SP
    M=D
    @13
    AM=M-1
    D=M
    @THAT
    M=D
    @13
    AM=M-1
    D=M
    @THIS
    M=D
    @13
    AM=M-1
    D=M
    @ARG
    M=D
    @13
    AM=M-1
    D=M
    @LCL
    M=D
    @14
    A=M
    0;JMP
(Main.fibonacci$IF_FALSE)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// DO_CALL: Main.fibonacci
    @RETFROM_Main.fibonacci2
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @6
    D=D-A
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @Main.fibonacci
    0;JMP
    (RETFROM_Main.fibonacci2)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
A=M-1
M=M-D
// DO_CALL: Main.fibonacci
    @RETFROM_Main.fibonacci3
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @6
    D=D-A
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @Main.fibonacci
    0;JMP
    (RETFROM_Main.fibonacci3)
@SP
AM=M-1
D=M
@SP
A=M-1
M=D+M
// DO_RETURN
    @LCL
    D=M
    @13
    M=D
    @5
    A=D-A
    D=M
    @14
    M=D
    @SP
    AM=M-1
    D=M
    @ARG
    A=M
    M=D
    @ARG
    D=M+1
    @SP
    M=D
    @13
    AM=M-1
    D=M
    @THAT
    M=D
    @13
    AM=M-1
    D=M
    @THIS
    M=D
    @13
    AM=M-1
    D=M
    @ARG
    M=D
    @13
    AM=M-1
    D=M
    @LCL
    M=D
    @14
    A=M
    0;JMP
@256
D=A
@SP
M=D
// DO_CALL: Sys.init
    @RETFROM_Sys.init4
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @5
    D=D-A
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @Sys.init
    0;JMP
    (RETFROM_Sys.init4)
// DO_FUNC
    (Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
// DO_CALL: Main.fibonacci
    @RETFROM_Main.fibonacci5
    D=A
    @SP
    AM=M+1
    A=A-1
    M=D
    @LCL
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @ARG
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THIS
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @THAT
    D=M
    @SP
    AM=M+1
    A=A-1
    M=D
    @SP
    D=M
    @6
    D=D-A
    @ARG
    M=D
    @SP
    D=M
    @LCL
    M=D
    @Main.fibonacci
    0;JMP
    (RETFROM_Main.fibonacci5)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP
