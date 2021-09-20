'''Evaluate the output of program with the expected output using various Metrices'''
from typing import Any, Dict, List, TYPE_CHECKING
from .metric import Equal, BaseMetrics
from .errors import CompilationError, RunTimeError

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from executioner.program import Program
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

    def to_json_object(self) -> Dict[str, Any]:
        '''Convert into JSON object'''
        return {
            "program": self.program.to_json_object(),
            "testcases": [testcase.to_json_object() for testcase in self.testcases],
            "metrics": [metric.to_json_object() for metric in self.metrics],
        }

    @staticmethod
    def from_json_object(data: Dict[str, Any]) -> 'Evaluation':
        '''Generate TestCase object from JSON object'''
        from executioner.program import Program  # pylint: disable=C0415
        return Evaluation(
            Program.from_json_object(data["program"]),
            testcases=[TestCase.from_json_object(
                test_obj) for test_obj in data["testcases"]],
            metrics=[BaseMetrics.from_json_object(
                metric_obj) for metric_obj in data['metrics'] if metric_obj]
        )

    def __eq__(self, o: 'Evaluation') -> bool:
        return (self.program == o.program) and all(
            [stest == otest for stest, otest in zip(
                self.testcases, o.testcases)]
        ) and all(
            [smetric == ometric for smetric, ometric in zip(
                self.metrics, o.metrics
            )]
        )

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

    def to_json_object(self) -> Dict[str, Any]:
        '''Convert into JSON object'''
        return {
            "input": self.input,
            "output": self.output,
            "real_output": self.real_output,
            "error": self.error.to_json_object() if self.error else None,
            "time": self.time,
            "scores": self.scores,
        }

    @staticmethod
    def from_json_object(data: Dict[str, Any]) -> 'TestCase':
        '''Generate TestCase object from JSON object'''
        testcase = TestCase(data["input"], data["output"])
        testcase.real_output = data.get("real_output", "")
        if data.get("error"):
            testcase.error = RunTimeError.from_json_object(data.get("error"))
        testcase.time = data.get("time", -1)
        testcase.scores = data.get("scores", dict())
        return testcase

    def __eq__(self, o: 'TestCase') -> bool:
        return all(
            [
                (self.input == o.input),
                (self.output == o.output),
                (self.error == o.error),
                (self.real_output == o.real_output),
            ]
        )

    def set_error(self, error):
        '''set error while evaluation'''
        self.error = error

    def set_scores(self, score_dict):
        '''set the scores for testcase for each metrics'''
        self.scores = score_dict
