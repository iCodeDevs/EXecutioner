'''represent a program'''
from typing import Any, Union
from executioner.settings import Settings
from executioner.sandbox.base_sandbox import SandBox
from executioner.sandbox.firejail import FireJail
from executioner.evaluate import TestCase


class CompiledProgram:

    '''compiled program class for file based sandboxing'''

    def __init__(self, lang_settings, compiled_file_location):
        '''initialize file location of compiled code'''
        self.lang_settings = lang_settings
        '''The language specific settings object'''
        self.file_location = compiled_file_location
        '''The file location of the compiled program after sandbox created it'''


class Program:

    '''Represent a program instance'''

    def __init__(self, pgm_obj: Union[str, Any], language: str, sandbox: SandBox = FireJail()):
        '''Create a new Program object'''

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
        self.compiled_program: CompiledProgram = None
        '''The compiled program object after compilation'''
        self.file_location: str = None
        '''The file location of the program after sandbox created it'''

    def compile(self) -> None:
        '''compile the program'''
        if not self.compiled_program:
            self.compiled_program = self.sandbox.compile(self)

    def execute(self, input_testcase: TestCase):
        '''execute the program'''
        return self.sandbox.execute(self, input_testcase)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self

    def __del__(self):
        '''Delete history and files of program in sandbox instance'''
        self.sandbox.delete(self)
