'''Evaluate the output of program with the expected output using various Metrices'''
from typing import List, TYPE_CHECKING
from src.metric.equal import Equal
from src.errors import CompilationError

if TYPE_CHECKING:
    from src.program import Program


class Evaluation:
    '''Evaluate the given program against Testcases and score with Metrics'''

    def __init__(self, program, testcases, metrics=None):
        self.program: 'Program' = program
        self.testcases: List[TestCase] = testcases
        self.metrics = metrics if metrics else [Equal()]

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

    def __init__(self, testcase_input, testcase_output=None):
        self.input = testcase_input
        self.output = testcase_output
        self.error = None
        self.scores = dict()

    def set_error(self, error):
        '''set error while evaluation'''
        self.error = error

    def set_scores(self, score_dict):
        '''set the scores for testcase for each metrics'''
        self.scores = score_dict
