'''
    A CLI script to run the library
'''

from  src.sandbox.firejail import FireJail
from src.program import Program
from src.evaluate import Evaluation, TestCase
program = Program('''
#include<stdio.h>
#include<stdlib.h>
int main(){
    char a[10];
    scanf("%s",a);
    printf("hello %s",a);
}
''', 'C', FireJail())

testcases = [TestCase("john", "hello john")]

evaluator = Evaluation(program, testcases)
evaluator.evaluate()

print(testcases[0].scores)
