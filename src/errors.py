'''Declare errors for different compilation and execution errors'''

class RunTimeError(Exception):
    '''represent runtime error of program'''


class CompilationError(Exception):
    '''represent compilation error of program'''


class MemoryOutError(Exception):
    '''represent memory error of program'''


class TimeOutError(Exception):
    '''represent time out error of program'''
