'''represent a program'''
from typing import Any, Union
from uuid import uuid4
from executioner.settings import Settings
from executioner.sandbox.base_sandbox import SandBox
from executioner.sandbox.firejail import FireJail
from executioner.evaluate import TestCase


class Program:

    '''Represent a program instance'''

    def __init__(self, pgm_obj: Union[str, Any], language: str, sandbox: SandBox = FireJail()):
        '''Create a new Program object'''

        self.uuid = uuid4()
        '''The unique id of this program'''

        self.language: str = language
        '''The language of the program'''
        self.code: str = ''
        '''The source code as a string'''
        if isinstance(pgm_obj, str):
            self.code: str = pgm_obj
        elif hasattr(pgm_obj, 'read'):
            self.code = pgm_obj.read()
            pgm_obj.close()

        self.settings = Settings.get_language_settings(language)
        '''The language specific settings object'''
        self.sandbox: SandBox = sandbox
        '''The sandbox to be used'''

    def compile(self) -> None:
        '''compile the program'''
        self.sandbox.compile(self)

    def execute(self, input_testcase: TestCase) -> None:
        '''execute the program'''
        self.sandbox.execute(self, input_testcase)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self

    def __del__(self):
        '''Delete history and files of program in sandbox instance'''
        self.sandbox.delete(self)
