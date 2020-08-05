import pytest

def raises_error(exception):
    def inner(func):
        def wrapper(*args,**kwargs):
            with pytest.raises(exception):
                func(*args,**kwargs)
        return wrapper
    return inner