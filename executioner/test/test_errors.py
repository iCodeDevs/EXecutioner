'''Test the errors module'''
import json
from executioner.errors import RunTimeError


class TestErrors():
    '''Test the error classes'''

    def test_json_coversion_with_args(self):
        '''test json conversion of errors with arguments'''
        err1 = RunTimeError("hello world")
        jsobj = err1.to_json_object()
        err2 = RunTimeError.from_json_object(json.loads(json.dumps(jsobj)))
        assert err1 == err2

    def test_json_coversion_without_args(self):
        '''test json conversion of errors without arguments'''
        err1 = RunTimeError()
        jsobj = err1.to_json_object()
        err2 = RunTimeError.from_json_object(json.loads(json.dumps(jsobj)))
        assert err1 == err2

    def test_json_coversion_of_non_error(self):
        '''test json conversion of non error objects to RunTimeError'''
        jsobj = {"class": ["executioner.program", "Program"]}
        err2 = RunTimeError.from_json_object(json.loads(json.dumps(jsobj)))
        assert err2 is None
