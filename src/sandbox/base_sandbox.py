'''Base sandbox class'''
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.evaluate import TestCase
    from src.program import Program


class SandBox:

    '''SandBox base class'''
    supported_languages = []

    def can_run(self, language: str):
        '''Check if the sandbox can this language'''
        return language in self.supported_languages

    def compile(self, program: 'Program', **kwarg):
        '''compile Program and return compiledProgram'''
        raise NotImplementedError

    def execute(self, program: 'Program', testcase: 'TestCase', **kwargs):
        '''execute the compiledProgram'''
        raise NotImplementedError

    def delete(self, program: 'Program', **kwargs):
        '''cleanup program related data from sandbox'''
        raise NotImplementedError
