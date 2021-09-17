'''defines the base metrics class'''
from typing import TYPE_CHECKING

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from src.evaluate import TestCase
#pylint: enable=W0611,R0401


class BaseMetrics:
    '''base class of Metrics'''

    def score(self, testcase: 'TestCase'):
        '''abstract score function to get score for given expected , recieved output'''
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__
