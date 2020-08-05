#A CLI script to run the library
from  src.sandbox.no_sandbox import NoSandBox
from src.Program import Program
import re
pgm = Program('''
#include<stdio.h>
#include<stdlib.h>
int main(){
    char a[10];
    scanf("%s",a);
    printf("hello %s",a);
}
''','C',NoSandBox())
pgm.compile()
print(pgm.execute('johnabraqw'))