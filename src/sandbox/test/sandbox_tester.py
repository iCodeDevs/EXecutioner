'''SandBox base test classes'''

from os import path
from src.evaluate import TestCase
from src.program import Program
from src.errors import RunTimeError, MemoryOutError, TimeOutError
from .decorators import raises_error


class BaseTestSandBox():

    '''Base Tests for all sandboxes'''

    sandbox = None


class SecureTestSandBox(BaseTestSandBox):

    '''Base Test file of all secure sandboxes'''

    def test_file_access(self):
        '''Test file access above workspace folder'''
        code = '''f = open('../a.txt', 'w')
f.write("hello world")
f.close()
'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase('')
        pgm.execute(testcase)
        file_path = path.join(path.dirname(pgm.file_location), '../a.txt')
        if path.exists(file_path):
            with open(file_path, 'r') as file_obj:
                assert file_obj.read().strip() != "hello world"
        else:
            assert True

    def test_network_access(self):
        '''Test network access of sandbox'''
        code = '''import http
conn = http.client.HTTPConnection('www.python.org')
conn.request("HEAD", "/index.html")
'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase('')
        pgm.execute(testcase)
        assert isinstance(testcase.error, RunTimeError)

    def test_memory_limit(self):
        '''Test memory limit of sandbox'''
        code = '''a = [i for i in range(1024*1024*1024)]'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase('')
        pgm.execute(testcase)
        assert isinstance(testcase.error, MemoryOutError)

    def test_runtime_limit(self):
        '''Test runtime limit of sandbox'''
        code = '''while(True):
    pass'''
        pgm = Program(code, 'python3', self.sandbox)
        pgm.compile()
        testcase = TestCase('')
        pgm.execute(testcase)
        assert isinstance(testcase.error, TimeOutError)

#     def test_tight_runtime_limit(self):
#         '''
#             Test the runtime limit tightly
#         '''
#         code = '''
# for i in range(int(input().strip())):
#     pass
#         '''
#         pgm = Program(code, 'python3', self.sandbox)
#         pgm.compile()
#         loops = 1
#         prev_time = 1
#         for _ in range(1, 30):
#             loops *= 10
#             testcase = TestCase(str(loops))
#             pgm.execute(testcase)
#             if isinstance(testcase.error, TimeOutError):
#                 last_loop = loops//10
#                 req_count = int(10*last_loop/prev_time) + (last_loop//10)
#                 print(testcase.time)
#                 break
#             prev_time = testcase.time
#             print(prev_time, _)

#         testcase = TestCase(str(req_count))
#         pgm.execute(testcase)
#         print(testcase.time)
#         assert isinstance(testcase.error, TimeOutError)
