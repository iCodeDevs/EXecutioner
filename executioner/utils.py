'''Utility functions'''
from typing import Any, Type, Union
import importlib


def get_import_path(obj: Any):
    '''get the import path of an object's class'''
    return (obj.__class__.__module__, obj.__class__.__qualname__)


def import_class(module: str, name: str) -> Union[Type, None]:
    '''get the class from given module with given name'''
    module = importlib.import_module(module)
    cls = getattr(module, name, None)
    if isinstance(cls, Type):
        return cls
    return None
