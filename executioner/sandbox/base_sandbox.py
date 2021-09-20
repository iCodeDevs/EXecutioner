'''Base sandbox class'''
from typing import TYPE_CHECKING, List, Tuple
from executioner.utils import import_class, get_import_path
#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from executioner.evaluate import TestCase
    from executioner.program import Program
#pylint: enable=W0611,R0401


class SandBox:

    '''SandBox base class'''
    supported_languages = []

    def compile(self, program: 'Program', **kwarg) -> None:
        '''compile the Program'''
        raise NotImplementedError

    def execute(self, program: 'Program', testcase: 'TestCase', **kwargs) -> None:
        '''execute the Program'''
        raise NotImplementedError

    def delete(self, program: 'Program', **kwargs) -> None:
        '''cleanup program related data from sandbox'''
        raise NotImplementedError

    def to_json_object(self) -> Tuple:
        '''convert to JSON object'''
        return get_import_path(self)

    @staticmethod
    def from_json_object(data: List) -> 'SandBox':
        '''Generate Program object from JSON object'''
        cls = import_class(*data)
        assert issubclass(cls, SandBox), "invalid Sandbox JSON"
        return cls()

    def __eq__(self, o: 'SandBox') -> bool:
        return get_import_path(self) == get_import_path(o)
