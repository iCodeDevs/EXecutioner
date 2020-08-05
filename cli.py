#A CLI script to run the library
from  src.sandbox.no_sandbox import NoSandBox
from src.Program import Program
from src.evaluate import Evaluation, TestCase
program = Program('''
#include<stdio.h>
#include<stdlib.h>
int main(){
    char a[10];
    scanf("%s",a);
    printf("hello %s",a);
}
''', 'C', NoSandBox())

testcases = [TestCase("john", "hello john")]

evaluator = Evaluation(program, testcases)
evaluator.evaluate()

print(testcases[0].scores)
