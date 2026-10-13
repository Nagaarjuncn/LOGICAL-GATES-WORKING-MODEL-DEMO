// logic.cpp
#include <iostream>

extern "C" {
    int logic_and(int a, int b) { return a & b; }
    int logic_or(int a, int b) { return a | b; }
    int logic_xor(int a, int b) { return a ^ b; }
    int logic_not(int a) { return !a; }
    int logic_nand(int a, int b) { return !(a & b); }
    int logic_nor(int a, int b) { return !(a | b); }
    int logic_xnor(int a, int b) { return !(a ^ b); }
}