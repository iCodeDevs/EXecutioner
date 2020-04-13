'''
Tests for settings module
'''
import json
import inspect
import os
import src

class TestLoaders:
    '''
    Collection of tests to check the settings loaders
    '''
    def test_load_default_settings(self):
        ''' Testing the load_default_settings function '''
        module_file = inspect.getfile(src)
        module_location = module_file[:module_file.rfind(os.path.sep)]
        settings_file = module_location+os.path.sep+"settings.json"
        expected_output = json.load(open(settings_file, 'r'))
        assert expected_output == src.settings.load_default_settings()

class TestCombineSettings:
    '''
    Tests to check combine_settings
    '''
    def test_empty_dictionary(self):
        ''' test with empty dictionary '''
        inputs = ({}, {})
        expected = {}
        assert expected == src.settings.combine_settings(*inputs)

    def test_nested_dictionary(self):
        ''' test with nested dictionary to depth 10 '''
        depth = 10
        main_dict = {'a': 1}
        added_dict = {'a': 2}
        expected = {'a': 2}
        inner_main_dict = None
        inner_added_dict = None
        inner_expected = None
        for _ in range(depth):
            assert expected == src.settings.combine_settings(main_dict, added_dict)
            if _ == 0:
                main_dict['a'] = {'a': 1}
                added_dict['a'] = {'a': 2}
                expected['a'] = {'a': 2}
                inner_main_dict = main_dict['a']
                inner_added_dict = added_dict['a']
                inner_expected = expected['a']
            else:
                inner_main_dict['a'] = {'a': 1}
                inner_added_dict['a'] = {'a': 2}
                inner_expected['a'] = {'a': 2}
                inner_main_dict = inner_main_dict['a']
                inner_added_dict = inner_added_dict['a']
                inner_expected = inner_expected['a']

    def test_empty_array(self):
        ''' test with empty array '''
        inputs = ([], [])
        expected = []
        assert expected == src.settings.combine_settings(*inputs)
