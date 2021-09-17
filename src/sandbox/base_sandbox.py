'''Base sandbox class'''
from typing import TYPE_CHECKING

#pylint: disable=W0611,R0401
if TYPE_CHECKING:
    from src.evaluate import TestCase
    from src.program import Program, CompiledProgram
#pylint: enable=W0611,R0401


class SandBox:

    '''SandBox base class'''
    supported_languages = []

    def can_run(self, language: str) -> bool:
        '''Check if the sandbox can this language'''
        return language in self.supported_languages

    def compile(self, program: 'Program', **kwarg) -> 'CompiledProgram':
        '''compile Program and return compiledProgram'''
        raise NotImplementedError

    def execute(self, program: 'Program', testcase: 'TestCase', **kwargs) -> None:
        '''execute the compiledProgram'''
        raise NotImplementedError

    def delete(self, program: 'Program', **kwargs) -> None:
        '''cleanup program related data from sandbox'''
        raise NotImplementedError
