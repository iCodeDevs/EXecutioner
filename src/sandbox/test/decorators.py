'''define decorators for internal use'''

import pytest


def raises_error(exception):
    '''pytest decorator to check if exception is raised in given function'''
    def inner(func):
        def wrapper(*args, **kwargs):
            with pytest.raises(exception):
                func(*args, **kwargs)
        return wrapper
    return inner
