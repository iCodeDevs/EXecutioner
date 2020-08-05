'''
General Tests for all SandBoxes
TODO:
    Make a General Test class for each language
'''
from src.Program import Program
from src.errors import CompilationError,RunTimeError,MemoryOutError,TimeOutError
from .decorators import raises_error
import pytest

class BaseTestSandBox():
    '''
    Base Tests for all sandboxes
    '''
    sandbox = None

class SecureTestSandBox(BaseTestSandBox):
    '''
    Base Test file of all secure sandboxes
    '''
#     @raises_error(RunTimeError)
#     def test_file_access(self):
#         code = '''f = open('a.txt','r')
# print(f.read())
# f.close()
# '''
#         pgm = Program(code,'python3',self.sandbox)
#         out=pgm.execute('')

    @raises_error(RunTimeError)
    def test_network_access(self):
        code = '''import http
conn = http.client.HTTPConnection('www.python.org')
conn.request("HEAD","/index.html")
'''
        pgm = Program(code,'python3',self.sandbox)
        pgm.execute('')

    @raises_error(MemoryOutError)
    def test_memory_limit(self):
        code = '''a = [i for i in range(1024*1024*1024)]'''
        pgm = Program(code,'python3',self.sandbox)
        pgm.execute('')

    @raises_error(TimeOutError)
    def test_runtime_limit(self):
        code = '''while(True):
    pass'''
        pgm = Program(code,'python3',self.sandbox)
        pgm.execute('')