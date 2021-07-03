#!/bin/bash

# You may need to apt install libxkbfile-dev

gcc -c -Wall -Werror -fpic keystate.c
gcc -shared -o libkeystate.so keystate.o
