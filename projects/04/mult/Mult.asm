// ============= @ADDRESS =======================
// @NNN or @xxx to set the address register to NNN or xxx

// =========== DEST=COMP;JUMP ====================
// COMP;JUMP 
// where depending on the value of COMP, 
// will jump to address specified in the A register
// or DEST=COMP
// in wich case the dest becomes the results of COMP


// numa = R0
// numb = R1
// result = R2


@R2
M=0

(LOOP)
    // if numb >0, loop
    @R1
    D=M
    @END
    D;JLE

    // result = result + numa 
    @R0
    D=M

    @R1
    A=M

    @R2
    M=D+M
    
    // numb--
    @R1
    M=M-1

    
    // else, end
    @LOOP
    0;JMP

(END)
    @END
    0;JMP
