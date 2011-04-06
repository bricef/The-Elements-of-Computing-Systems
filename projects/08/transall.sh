#! /bin/bash
./vm/S2VM.py ./ProgramFlow/FibonacciSeries/FibonacciSeries.vm > ./ProgramFlow/FibonacciSeries/FibonacciSeries.asm
./vm/S2VM.py ./ProgramFlow/BasicLoop/BasicLoop.vm > ./ProgramFlow/BasicLoop/BasicLoop.asm
./vm/S2VM.py ./FunctionCalls/FibonacciElement/ > ./FunctionCalls/FibonacciElement/FibonacciElement.asm
./vm/S2VM.py ./FunctionCalls/StaticsTest/ > ./FunctionCalls/StaticsTest/StaticsTest.asm
./vm/S2VM.py ./FunctionCalls/SimpleFunction/SimpleFunction.vm > ./FunctionCalls/SimpleFunction/SimpleFunction.asm
./vm/S2VM.py ./own-test/functest.vm > ./own-test/functest.asm
./vm/S2VM.py ./own-test/test.vm > ./own-test/test.asm
