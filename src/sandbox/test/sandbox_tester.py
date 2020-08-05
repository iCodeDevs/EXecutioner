'''SandBox base test classes'''

from os import path
from src.program import Program
from src.errors import RunTimeError, MemoryOutError, TimeOutError
from .decorators import raises_error

class BaseTestSandBox():

    '''Base Tests for all sandboxes'''

    sandbox = None

class SecureTestSandBox(BaseTestSandBox):

    '''Base Test file of all secure sandboxes'''

    @raises_error(RunTimeError)
    def test_file_access(self):
        '''Test file access above workspace folder'''
        code = '''f = open('../a.txt', 'w')
f.write("hello world")
f.close()
'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        pgm.execute('')
        file_path = path.join(path.dirname(pgm.file_location), '../a.txt')
        if path.exists(file_path):
            with open(file_path, 'r') as file_obj:
                assert file_obj.read().strip() != "hello world"
        else:
            assert True

    @raises_error(RunTimeError)
    def test_network_access(self):
        '''Test network access of sandbox'''
        code = '''import http
conn = http.client.HTTPConnection('www.python.org')
conn.request("HEAD", "/index.html")
'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        pgm.execute('')

    @raises_error(MemoryOutError)
    def test_memory_limit(self):
        '''Test memory limit of sandbox'''
        code = '''a = [i for i in range(1024*1024*1024)]'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        pgm.execute('')

    @raises_error(TimeOutError)
    def test_runtime_limit(self):
        '''Test runtime limit of sandbox'''
        code = '''while(True):
    pass'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        pgm.execute('')
