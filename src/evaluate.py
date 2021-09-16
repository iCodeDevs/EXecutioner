'''Evaluate the output of program with the expected output using various Metrices'''
from typing import List, TYPE_CHECKING
from src.metric.equal import Equal
from src.errors import CompilationError, RunTimeError

if TYPE_CHECKING:
    from src.program import Program
    from src.metric.base import BaseMetrics


class Evaluation:
    '''Evaluate the given program against Testcases and score with Metrics'''

    def __init__(
            self,
            program: 'Program',
            testcases: List['TestCase'],
            metrics: List['BaseMetrics'] = None
    ):
        self.program: 'Program' = program
        self.testcases: List['TestCase'] = testcases
        self.metrics: List['BaseMetrics'] = metrics if metrics else [Equal()]

    def evaluate(self):
        '''Evaluate the program against testcases and return testcases with scores'''
        try:
            self.program.compile()
        except CompilationError:
            for testcase in self.testcases:
                testcase.set_error('compilation error')
            return self.testcases

        for testcase in self.testcases:
            recv_output = self.program.execute(testcase)
            scores = self.get_scores(testcase.output, recv_output)
            testcase.set_scores(scores)
        return self.testcases

    def get_scores(self, exp_output, recv_output):
        '''Run metrics for outputs'''
        score_dict = dict()
        for metric in self.metrics:
            score = metric.score(exp_output, recv_output)
            score_dict[str(metric)] = score
        return score_dict


class TestCase:
    '''Represent a testcase'''

    def __init__(self, testcase_input='', testcase_output=''):
        self.input: str = testcase_input
        self.output: str = testcase_output

        self.real_output: str = ''

        self.error: RunTimeError = None
        self.time: float = -1
        self.scores = dict()

    def set_error(self, error):
        '''set error while evaluation'''
        self.error = error

    def set_scores(self, score_dict):
        '''set the scores for testcase for each metrics'''
        self.scores = score_dict
