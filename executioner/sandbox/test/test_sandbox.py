'''Tests for NoSandBox sandbox'''

from executioner.sandbox.no_sandbox import NoSandBox
from executioner.sandbox.firejail import FireJail
from .sandbox_tester import SecureTestSandBox
from .language_tester import PythonTestSandBox, CTestSandBox


class TestNoSandBox(CTestSandBox, PythonTestSandBox):
    '''Tests for NoSandBox class'''
    sandbox = NoSandBox()


class TestFireJail(CTestSandBox, PythonTestSandBox, SecureTestSandBox):
    '''Tests for FireJail class'''
    sandbox = FireJail()
