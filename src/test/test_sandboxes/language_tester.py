from src.Program import Program
from src.errors import CompilationError,RunTimeError,MemoryOutError,TimeOutError
from .sandbox_tester import BaseTestSandBox
from .decorators import raises_error
import pytest
import os

def ls():
    print('playground:')
    for i in os.walk('playground'):
        print("--",i)

class PythonTestSandBox(BaseTestSandBox):
    ''' Tests for Python Language '''
    def test_python_success(self):
        code = '''print("hello world")'''
        expected_out = "hello world"
        inp = ""
        pgm = Program(code,'python3',self.sandbox)
        out = pgm.execute(inp)
        assert expected_out == out.strip()

    @raises_error(RunTimeError)
    def test_python_error(self):
        code = '''a = 1/0'''
        inp = ""
        pgm = Program(code,'python3',self.sandbox)
        out = pgm.execute(inp)


class CTestSandBox(BaseTestSandBox):
    ''' Tests for C Language '''
    def test_c_success(self):
        code = '''
        #include<stdio.h>
        int main(){
            printf("hello world");
            return 0;
        }
        '''
        expected_out = "hello world"
        inp = ""
        pgm = Program(code,'C',self.sandbox)
        out = pgm.execute(inp)
        assert expected_out == out

    @raises_error(RunTimeError)
    def test_c_error(self):
        code = '''
        #include<stdio.h>
        int main(){
            int a,b;
            scanf("%d",&b);
            a = 10/b;
            return 0;
        }
        '''
        expected_out = "hello world"
        inp = "0"
        pgm = Program(code,'C',self.sandbox)
        out = pgm.execute(inp)

    @raises_error(CompilationError)
    def test_c_compilation_error(self):
        code = '''
        #include<stdio.h>
        int main(){
            printf("hello world")
            return 0;
        }
        '''
        expected_out = "hello world"
        inp = ""
        Program(code,'C',self.sandbox)