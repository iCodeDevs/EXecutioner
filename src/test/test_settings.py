'''
Tests for settings module
'''
# pylint: disable=R0201,R0903

import json
import inspect
import os
from pytest import raises
import src

class TestLoaders:

    '''Collection of tests to check the settings loaders'''

    def test_load_default_settings(self):
        '''Testing the load_default_settings function'''
        module_file = inspect.getfile(src)
        module_location = module_file[:module_file.rfind(os.path.sep)]
        settings_file = module_location+os.path.sep+"settings.json"
        expected_output = json.load(open(settings_file, 'r'))
        assert expected_output == src.settings.load_default_settings()

class TestCombineSettings:
    '''Tests to check combine_settings'''

    def nested_dictionary_generator(self, depth):
        '''Nested dictionary generator'''
        main_dict = {}
        added_dict = {}
        expected = {}
        inner_main_dict = None
        inner_added_dict = None
        inner_expected = None
        for _ in range(depth):
            yield main_dict, added_dict, expected
            if _ == 0:
                main_dict['a'] = {'a': 1, 'b': 2}
                added_dict['a'] = {'a': 2, 'c': 3}
                expected['a'] = {'a': 2, 'b': 2}
                inner_main_dict = main_dict['a']
                inner_added_dict = added_dict['a']
                inner_expected = expected['a']
            else:
                inner_main_dict['a'] = {'a': 1, 'b': 2}
                inner_added_dict['a'] = {'a': 2, 'c': 3}
                inner_expected['a'] = {'a': 2, 'b': 2}
                inner_main_dict = inner_main_dict['a']
                inner_added_dict = inner_added_dict['a']
                inner_expected = inner_expected['a']

    def test_nested_dictionary(self):
        '''test with nested dictionary to depth 10 including empty'''
        depth = 11
        testcases = self.nested_dictionary_generator(depth)
        for main_dict, added_dict, expected in testcases:
            assert expected == src.settings.combine_settings(main_dict, added_dict)

    def test_combination_dictionary(self):
        '''test combination of dictionaries'''
        main_dict = {
            'a':{
                'b':2,
                'c':{
                    'd':1,
                }
            },
            'b':2,
            'c':3
        }
        added_dict = {
            'a': {
                'c': {
                    'd': 2,
                }
            }
        }
        expected = {
            'a':{
                'b':2,
                'c':{
                    'd':2,
                }
            },
            'b':2,
            'c':3
        }
        assert expected == src.settings.combine_settings(main_dict, added_dict)

    def test_empty_array(self):
        '''test with empty array'''
        inputs = ([], [])
        expected = []
        assert expected == src.settings.combine_settings(*inputs)

    def test_array_join(self):
        '''test array join'''
        inputs = ([1, 2], [3, 4])
        expected = [1, 2, 3, 4]
        assert expected == src.settings.combine_settings(*inputs)

    def test_array_dictionary(self):
        '''test combination of array and dictionary'''
        main_dict = {
            'a':{
                'b':2,
                'c':{
                    'd':1,
                }
            },
            'b':2,
            'c':[1, 2]
        }
        added_dict = {
            'a': {
                'c': {
                    'd': 2,
                }
            },
            'c': [3, 4]
        }
        expected = {
            'a':{
                'b':2,
                'c':{
                    'd':2,
                }
            },
            'b':2,
            'c':[1, 2, 3, 4]
        }
        assert expected == src.settings.combine_settings(main_dict, added_dict)

    def test_incompatible_types(self):
        '''checking if incompatible type error is thrown'''
        with raises(Exception) as error:
            src.settings.combine_settings({}, [])
        assert str(error.value) == 'incompatible types'
