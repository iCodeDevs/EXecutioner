'''Tests for NoSandBox sandbox'''
from pathlib import Path
from executioner.sandbox.no_sandbox import NoSandBox
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
            Settings.load_added_settings(f'workspace: {str(tmp_path.joinpath("fake"))}')
            pgm.compile()
            Settings.load_added_settings('workspace: playground')


class TestFireJail(CTestSandBox, PythonTestSandBox, SecureTestSandBox):
    '''Tests for FireJail class'''
    sandbox = FireJail()
