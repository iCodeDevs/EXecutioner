'''Evaluation Metrics module'''
from typing import TYPE_CHECKING, Tuple, List, Union
from executioner.utils import get_import_path, import_class
#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from executioner.evaluate import TestCase
#pylint: enable=W0611,R0401


class BaseMetrics:
    '''base class of Metrics'''

    def score(self, testcase: 'TestCase'):
        '''abstract score function to get score for given expected , recieved output'''
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

    def to_json_object(self) -> Tuple:
        '''convert to JSON object'''
        return get_import_path(self)

    @staticmethod
    def from_json_object(data: List) -> Union['BaseMetrics', None]:
        '''Generate Program object from JSON object'''
        cls = import_class(*data)
        if not issubclass(cls, BaseMetrics):
            return None
        else:
            return cls()

    def __eq__(self, o: 'BaseMetrics') -> bool:
        return get_import_path(self) == get_import_path(o)


class Equal(BaseMetrics):
    '''a 0/1 metric, gives full score if equal'''

    def score(self, testcase: 'TestCase'):
        if testcase.output.strip() == testcase.real_output.strip():
            return 1
        return 0
