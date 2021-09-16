'''
Tests for settings module
'''
# pylint: disable=R0201,R0903

import json
import inspect
import os
import src
from src.settings import Settings


class TestLoaders:

    '''Collection of tests to check the settings loaders'''

    def test_load_default_settings(self):
        '''Testing the load_default_settings function'''
        module_file = inspect.getfile(src)
        module_location = module_file[:module_file.rfind(os.path.sep)]
        settings_file = module_location+os.path.sep+"settings.json"
        expected_output = json.load(open(settings_file, 'r'))
        Settings.load_default_settings()
        assert expected_output == Settings.SETTINGS
