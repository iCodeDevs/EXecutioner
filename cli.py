'''
    A CLI script to run the library
'''

from executioner.sandbox.firejail import FireJail
from executioner.program import Program
from executioner.evaluate import TestCase

pgm = Program("print('hello world')", 'python3', FireJail())
pgm.compile()
testcase = TestCase()
pgm.execute(testcase)
print(testcase.real_output)
