'''Tests for evaluate Module'''

from executioner.evaluate import Evaluation, TestCase
from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.metric import Equal
from executioner.errors import CompilationError


class TestEvaluation():
    '''Test the Evaluation Class'''

    def test_evaluate_success(self):
        '''Test evaluate success'''
        code = '''
print("hello world")
'''
        pgm = Program(code, 'python3', FireJail())
        testcases = [TestCase(testcase_output='hello world')]
        ev_obj = Evaluation(
            pgm,
            testcases,
            [Equal()],
        )
        ev_obj.evaluate()
        assert testcases[0].scores == {'Equal': 1}

    def test_evaluate_compilation(self):
        '''Test evaluate compilation error'''
        code = '''
print("hello world"
'''
        pgm = Program(code, 'python3', FireJail())
        testcases = [TestCase(testcase_output='hello world')]
        ev_obj = Evaluation(
            pgm,
            testcases,
            [Equal()],
        )
        ev_obj.evaluate()
        assert all([isinstance(test.error, CompilationError)
                    for test in testcases])
