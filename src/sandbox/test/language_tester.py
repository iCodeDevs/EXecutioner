from src.Program import Program
from src.errors import CompilationError,RunTimeError
from .sandbox_tester import BaseTestSandBox
from .decorators import raises_error

class PythonTestSandBox(BaseTestSandBox):

    '''Tests for Python Language'''

    def test_python_success(self):
        code = '''print("hello world")'''
        expected_out = "hello world"
        inp = ""
        pgm = Program(code,'python3',self.sandbox)
        pgm.compile()
        out = pgm.execute(inp)
        assert expected_out == out.strip()

    @raises_error(RunTimeError)
    def test_python_error(self):
        code = '''a = 1/0'''
        inp = ""
        pgm = Program(code,'python3',self.sandbox)
        pgm.compile()
        pgm.execute(inp)


class CTestSandBox(BaseTestSandBox):

    '''Tests for C Language'''

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
        pgm.compile()
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
        inp = "0"
        pgm = Program(code,'C',self.sandbox)
        pgm.compile()
        pgm.execute(inp)

    @raises_error(CompilationError)
    def test_c_compilation_error(self):
        code = '''
        #include<stdio.h>
        int main(){
            printf("hello world")
            return 0;
        }
        '''
        pgm = Program(code,'C',self.sandbox)
        pgm.compile()