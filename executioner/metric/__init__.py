'''Evaluation Metrics module'''
from typing import TYPE_CHECKING

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


class Equal(BaseMetrics):
    '''a 0/1 metric, gives full score if equal'''

    def score(self, testcase: 'TestCase'):
        if testcase.output.strip() == testcase.real_output.strip():
            return 1
        return 0
