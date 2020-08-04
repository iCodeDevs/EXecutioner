'''
Declare errors for different compilation and execution errors
'''
# Cannot Compile Error

class RunTimeError(Exception):
    pass

class CompilationError(Exception):
    pass

class MemoryOutError(Exception):
    pass

class TimeOutError(Exception):
    pass