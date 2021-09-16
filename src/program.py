'''represent a program'''
from typing import Any, Union
from src.settings import Settings
from src.sandbox.base_sandbox import SandBox
from src.sandbox.firejail import FireJail
from src.evaluate import TestCase


class CompiledProgram:

    '''compiled program class for file based sandboxing'''

    def __init__(self, lang_settings, compiled_file_location):
        '''initialize file location of compiled code'''
        self.lang_settings = lang_settings
        self.file_location = compiled_file_location


class Program:

    '''Represent a program instance'''

    def __init__(self, pgm_obj: Union[str, Any], language: str, sandbox: SandBox = FireJail()):
        self.language: str = language
        if isinstance(pgm_obj, str):
            self.code: str = pgm_obj
        elif hasattr(pgm_obj, 'read'):
            self.code = pgm_obj.read()
            pgm_obj.close()

        self.settings = Settings.get_language_settings(language)
        self.sandbox: SandBox = sandbox
        self.compiled_program = None
        self.file_location = None

    def compile(self) -> None:
        '''compile the program'''
        if not self.compiled_program:
            self.compiled_program = self.sandbox.compile(self)

    def execute(self, input_testcase: TestCase):
        '''execute the program'''
        return self.sandbox.execute(self, input_testcase)

    def __del__(self):
        '''Delete history and files of program in sandbox instance'''
        self.sandbox.delete(self)
