'''
    A CLI script to run the library
'''

from src.sandbox.firejail import FireJail
from src.program import Program
from src.evaluate import TestCase

with Program('''
print("hello world")
''', 'python3', FireJail()) as PROGRAM:
    TESTCASE = TestCase("hello world")
    PROGRAM.compile()
    PROGRAM.execute(TESTCASE)
    print(TESTCASE.real_output)
