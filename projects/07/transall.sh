#! /bin/bash
./S1VM.py ./MemoryAccess/BasicTest/BasicTest.vm > ./MemoryAccess/BasicTest/BasicTest.asm
./S1VM.py ./MemoryAccess/StaticTest/StaticTest.vm > ./MemoryAccess/StaticTest/StaticTest.asm
./S1VM.py ./MemoryAccess/PointerTest/PointerTest.vm > ./MemoryAccess/PointerTest/PointerTest.asm
./S1VM.py ./StackArithmetic/StackTest/StackTest.vm > ./StackArithmetic/StackTest/StackTest.asm
./S1VM.py ./StackArithmetic/SimpleAdd/SimpleAdd.vm > ./StackArithmetic/SimpleAdd/SimpleAdd.asm

