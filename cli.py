'''
    A CLI script to run the library
'''

from src.sandbox.firejail import FireJail
from src.program import Program
from src.evaluate import Evaluation, TestCase
PROGRAM = Program('''
#include<stdio.h>
#include<stdlib.h>
int main(){
    char a[10];
    scanf("%s",a);
    printf("hello %s",a);
}
''', 'C', FireJail())

TESTCASES = [TestCase("john", "hello john")]

EVALUATOR = Evaluation(PROGRAM, TESTCASES)
EVALUATOR.evaluate()

print(TESTCASES[0].scores)
