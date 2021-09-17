'''define Equal Metrics class'''

from typing import TYPE_CHECKING
from .base import BaseMetrics


#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from src.evaluate import TestCase
#pylint: enable=W0611,R0401


class Equal(BaseMetrics):
    '''a 0/1 metric, gives full score if equal'''

    def score(self, testcase: 'TestCase'):
        if testcase.output.strip() == testcase.real_output.strip():
            return 1
        return 0
