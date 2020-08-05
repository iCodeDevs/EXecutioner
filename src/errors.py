'''Declare errors for different compilation and execution errors'''

class RunTimeError(Exception):
    pass

class CompilationError(Exception):
    pass

class MemoryOutError(Exception):
    pass

class TimeOutError(Exception):
    pass