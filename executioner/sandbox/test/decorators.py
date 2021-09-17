'''define decorators for internal use'''

import pytest


def raises_error(exception):
    '''pytest decorator to check if exception is raised in given function'''
    def inner(func):
        '''inner function'''
        def wrapper(*args, **kwargs):
            '''Wrapper function'''
            with pytest.raises(exception):
                func(*args, **kwargs)
        return wrapper
    return inner
