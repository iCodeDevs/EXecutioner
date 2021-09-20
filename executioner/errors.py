'''Declare errors for different compilation and execution errors'''
from typing import Dict, Any
from .utils import get_import_path, import_class


class RunTimeError(Exception):
    '''represent runtime error of program'''

    def to_json_object(self) -> Dict[str, Any]:
        '''Convert into JSON object'''
        return {
            'class': get_import_path(self),
            'text': str(self),
        }

    @staticmethod
    def from_json_object(data: Dict[str, Any]) -> 'RunTimeError':
        '''Generate TestCase object from JSON object'''
        assert "class" in data and "text" in data, "invalid RunTimeError JSON"
        cls = import_class(*data['class'])
        assert issubclass(cls, RunTimeError), "invalid RunTimeError JSON"
        if not data.get("text"):
            return cls()
        return cls(data.get("text"))

    def __eq__(self, o: object) -> bool:
        return self.__class__.__name__ == o.__class__.__name__ and str(self) == str(o)


class CompilationError(RunTimeError):
    '''represent compilation error of program'''


class MemoryOutError(RunTimeError):
    '''represent memory error of program'''


class TimeOutError(RunTimeError):
    '''represent time out error of program'''
