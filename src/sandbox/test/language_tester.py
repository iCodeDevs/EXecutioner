'''Languagewise Test Classes'''

from src.evaluate import TestCase
from src.program import Program
from src.errors import CompilationError, RunTimeError
from .sandbox_tester import BaseTestSandBox
from .decorators import raises_error


class PythonTestSandBox(BaseTestSandBox):

    '''Tests for Python Language'''

    def test_python_success(self):
        '''test successful python code'''
        code = '''print("hello world")'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase(testcase_output="hello world")
        pgm.execute(testcase)
        assert testcase.real_output.strip() == testcase.output

    def test_python_error(self):
        '''test runtime error in python'''
        code = '''a = 1/0'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase()
        pgm.execute(testcase)
        assert isinstance(testcase.error, RunTimeError)


class CTestSandBox(BaseTestSandBox):

    '''Tests for C Language'''

    def test_c_success(self):
        '''test successful C code'''
        code = '''
        #include<stdio.h>
        int main(){
            printf("hello world");
            return 0;
        }
        '''
        pgm = Program(code, 'C', self.sandbox)
        pgm.compile()
        testcase = TestCase(testcase_output="hello world")
        pgm.execute(testcase)
        assert testcase.real_output.strip() == testcase.output

    def test_c_error(self):
        '''test runtime error in C'''
        code = '''
        #include<stdio.h>
        int main(){
            int a, b;
            scanf("%d", &b);
            a = 10/b;
            return 0;
        }
        '''
        pgm = Program(code, 'C', self.sandbox)
        pgm.compile()
        testcase = TestCase("0")
        pgm.execute(testcase)
        assert isinstance(testcase.error, RunTimeError)

    @raises_error(CompilationError)
    def test_c_compilation_error(self):
        '''Test compilation error in C'''
        code = '''
        #include<stdio.h>
        int main(){
            printf("hello world")
            return 0;
        }
        '''
        pgm = Program(code, 'C', self.sandbox)
        pgm.compile()
