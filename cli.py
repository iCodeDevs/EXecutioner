'''
    A CLI script to run the library
'''

from src.sandbox.firejail import FireJail
from src.program import Program
from src.evaluate import Evaluation, TestCase
PROGRAM = Program('''
print("hello world")
''', 'python3', FireJail())

TESTCASE = TestCase("hello world")
PROGRAM.compile()
PROGRAM.execute(TESTCASE)

print(TESTCASE.real_output)

del PROGRAM