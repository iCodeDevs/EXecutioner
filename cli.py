'''
    A CLI script to run the library
'''

from src.sandbox.firejail import FireJail
from src.program import Program
from src.evaluate import TestCase

pgm = Program("print('hello world')", 'python3', FireJail())
pgm.compile()
testcase = TestCase()
pgm.execute(testcase)
print(testcase.real_output)
