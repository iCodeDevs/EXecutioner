'''Tests for the basic metrics'''
import json
from executioner.metric import Equal, BaseMetrics
from executioner.evaluate import TestCase


class TestBaseMetrics():
    '''Test BaseMetrics class'''

    def test_json_conversion(self):
        '''Test json conversion'''
        metric1 = BaseMetrics()
        jsobj = metric1.to_json_object()
        metric2 = BaseMetrics.from_json_object(json.loads(json.dumps(jsobj)))
        assert metric1 == metric2

    def test_json_conversion_non_metric(self):
        '''test json conversion of non metric class'''
        jsobj = ["executioner.program", "Program"]
        metric1 = BaseMetrics.from_json_object(jsobj)
        assert metric1 is None


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
