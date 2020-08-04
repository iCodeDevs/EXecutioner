'''
Tests for NoSandBox sandbox
'''
from .sandbox_tester import SecureTestSandBox
from .language_tester import PythonTestSandBox, CTestSandBox
from src.sandbox.no_sandbox import NoSandBox
from src.sandbox.firejail import FireJail

class TestNoSandBox(CTestSandBox,PythonTestSandBox):
    sandbox = NoSandBox()

class TestFireJail(CTestSandBox, PythonTestSandBox, SecureTestSandBox):
    sandbox = FireJail()