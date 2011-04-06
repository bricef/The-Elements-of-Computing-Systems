(MAINLOOP)
    @KBD
    D=M
    @FILLWHITE
    D;JGT
    @FILLBLACK
    0;JMP

(FILLWHITE)
    @SCREEN
    D=A
    (FWLOOP)
        A=D
        M=0
        D=A+1
        @R1 //store screen pointer
        M=D
            @24575
            D=D-A
            @MAINLOOP //if its too high, all done, jump to mainloop
            D;JGT
        @R1 //restore screen pointer
        D=M
        @FWLOOP
        0;JMP

(FILLBLACK)
    @SCREEN
    D=A
    (FBLOOP)
        A=D
        M=-1
        D=A+1
        @R1 //store screen pointer
        M=D
            @24575
            D=D-A
            @MAINLOOP //if its too high, all done, jump to mainloop
            D;JGT
        @R1 //restore screen pointer
        D=M
        @FBLOOP
        0;JMP
