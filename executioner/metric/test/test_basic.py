'''Tests for the basic metrics'''

from executioner.metric import Equal
from executioner.evaluate import TestCase


class TestEqual():
    '''Test Equal metrics'''
    mobj = Equal()

    def test_equal(self):
        '''if equal'''
        testcase = TestCase(testcase_output="hello world")
        testcase.real_output = "hello world"
        assert self.mobj.score(testcase) == 1

    def test_unequal(self):
        '''if unequal'''
        testcase = TestCase(testcase_output="hello world")
        testcase.real_output = "hello not world"
        assert self.mobj.score(testcase) == 0

    def test_space_ignore(self):
        '''does it ignore space'''
        testcase = TestCase(testcase_output="hello world")
        testcase.real_output = '''hello world
        '''
        assert self.mobj.score(testcase) == 1
