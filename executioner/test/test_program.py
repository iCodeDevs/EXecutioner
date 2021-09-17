'''Test for Program class'''
from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.evaluate import TestCase


class TestProgram():
    '''Test class for Program Class'''

    def test_basic_usage(self):
        '''test basic usage of Program class'''
        pgm = Program("print('hello world')", 'python3', FireJail())
        pgm.compile()
        testcase = TestCase()
        pgm.execute(testcase)
        assert testcase.real_output.strip() == "hello world"

    def test_context_manager_usage(self):
        '''Test usage of Program class as context manager'''
        with Program("print('hello world')", 'python3', FireJail()) as pgm:
            pgm.compile()
            testcase = TestCase()
            pgm.execute(testcase)
            assert testcase.real_output.strip() == "hello world"
