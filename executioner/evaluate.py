'''Evaluate the output of program with the expected output using various Metrices'''
from typing import Dict, List, TYPE_CHECKING
from .metric import Equal
from .errors import CompilationError, RunTimeError

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from executioner.program import Program
    from executioner.metric import BaseMetrics
#pylint: enable=W0611,R0401


class Evaluation:
    '''Evaluate the given program against Testcases and score with Metrics'''

    def __init__(
            self,
            program: 'Program',
            testcases: List['TestCase'],
            metrics: List['BaseMetrics'] = None
    ):
        '''Create a new Evaluation object'''
        self.program: 'Program' = program
        '''The program being evaluated'''
        self.testcases: List['TestCase'] = testcases
        '''the list of testcase to execute the program on'''
        self.metrics: List['BaseMetrics'] = metrics if metrics else [Equal()]
        '''The list of metrices to evaluate the program on'''

    def evaluate(self):
        '''Evaluate the program against testcases and return testcases with scores'''
        try:
            self.program.compile()
        except CompilationError:
            for testcase in self.testcases:
                testcase.set_error(CompilationError())
            return self.testcases

        for testcase in self.testcases:
            self.program.execute(testcase)
            scores = self.get_scores(testcase)
            testcase.set_scores(scores)
        return self.testcases

    def get_scores(self, testcase: 'TestCase'):
        '''Run metrics for outputs'''
        score_dict = dict()
        for metric in self.metrics:
            score = metric.score(testcase)
            score_dict[str(metric)] = score
        return score_dict


class TestCase:
    '''Represent a testcase'''

    def __init__(self, testcase_input='', testcase_output=''):
        '''Create a new testcase using given input and output'''

        self.input: str = testcase_input
        ''' input for this testcase '''
        self.output: str = testcase_output
        ''' expected output for this testcase '''

        self.real_output: str = ''
        '''real output for this testcase after execution'''

        self.error: RunTimeError = None
        '''error received after execution'''
        self.time: float = -1
        '''time taken to execute'''
        self.scores: Dict[str, int] = dict()
        '''The score Dictionary Object'''

    def set_error(self, error):
        '''set error while evaluation'''
        self.error = error

    def set_scores(self, score_dict):
        '''set the scores for testcase for each metrics'''
        self.scores = score_dict
