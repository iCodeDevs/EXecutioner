'''Test the utils module'''

from executioner.utils import get_import_path, import_class

VAR_FOR_TESTING = 1


class TestUtils():
    '''Test the utilties functions'''

    def test_get_import(self):
        '''Test get import and import class together'''
        res = get_import_path(self)
        cls = import_class(*res)
        assert self.__class__ == cls

    def test_non_class_import(self):
        '''Test non class import'''
        res = [self.__class__.__module__, "VAR_FOR_TESTING"]
        cls = import_class(*res)
        assert cls is None
