// ============= @ADDRESS =======================
// @NNN or @xxx to set the address register to NNN or xxx

// =========== DEST=COMP;JUMP ====================
// COMP;JUMP 
// where depending on the value of COMP, 
// will jump to address specified in the A register
// or DEST=COMP
// in wich case the dest becomes the results of COMP


// 
// fill screen when key pressed.
// Screen begins ast 16384 @SCREEN
// and ends at 24575
// the keybord is at 24576 and @KBD

(BEGIN)
@SCREEN
D=A
(LOOP)
    //
    // check kbd
    //
    @R1 //store screen pointer
    M=D
        //if @KBD is >0;
        // let M[D]=0  jmp continue
        //else
        // let M[D]=-1 jmp continue
    
        @KBD
        D=M
        @KEYPRESS //if keypress, jump to keypress
        D;JGT
        @NOTKEYPRESS //if not key, jump to motkeypress
        D;JLE
        
        (KEYPRESS)  
            @R1
            A=M
            M=0
            @DONEPAINT
            0;JMP
        
        (NOTKEYPRESS)
            @R1
            A=M
            M=-1
            @DONEPAINT
            0;JMP
        
        (DONEPAINT)

    @R1 //restore screen pointer
    D=M
    D=M+1


    
    (CONTINUE)
    
    //
    //check that D isnt too high!
    //
    @R1 //store screen pointer
    M=D
        @24575
        D=D-A
        @BEGIN
        D;JGT
    @R1 //restore screen pointer
    D=M
    
    @LOOP
    0;JMP


(END)
    @END
    0;JMP

