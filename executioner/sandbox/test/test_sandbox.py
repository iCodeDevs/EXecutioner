'''Tests for NoSandBox sandbox'''
from pathlib import Path
import json
from executioner.sandbox.no_sandbox import NoSandBox, SandBox
from executioner.sandbox.firejail import FireJail
from executioner.settings import Settings
from executioner.program import Program
from .sandbox_tester import SecureTestSandBox
from .language_tester import PythonTestSandBox, CTestSandBox


class TestNoSandBox(CTestSandBox, PythonTestSandBox):
    '''Tests for NoSandBox class'''
    sandbox = NoSandBox()

    def test_no_workspace(self, tmp_path: Path):
        '''Test if workspace does not exist'''
        with Program("print('hello world')", 'python3', self.sandbox) as pgm:
            Settings.load_added_settings(
                f'workspace: {str(tmp_path.joinpath("fake"))}')
            pgm.compile()
            Settings.load_added_settings('workspace: playground')


class TestFireJail(CTestSandBox, PythonTestSandBox, SecureTestSandBox):
    '''Tests for FireJail class'''
    sandbox = FireJail()


class TestSandBox():
    '''Test SandBox class'''

    def test_json_conversion(self):
        '''Test json conversion'''
        sbox1 = SandBox()
        jsobj = sbox1.to_json_object()
        sbox2 = SandBox.from_json_object(json.loads(json.dumps(jsobj)))
        assert sbox1 == sbox2

    def test_json_conversion_non_sandbox(self):
        '''test json conversion of non sandbox class'''
        jsobj = ["executioner.program", "Program"]
        metric1 = SandBox.from_json_object(jsobj)
        assert metric1 is None
