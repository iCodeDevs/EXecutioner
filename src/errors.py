'''Declare errors for different compilation and execution errors'''


class RunTimeError(Exception):
    '''represent runtime error of program'''


class CompilationError(RunTimeError):
    '''represent compilation error of program'''


class MemoryOutError(RunTimeError):
    '''represent memory error of program'''


class TimeOutError(RunTimeError):
    '''represent time out error of program'''

class NotCompiledError(Exception):
    '''Raised if the Program is not compiled before execution'''
