'''Tests for settings module'''
import pytest
from executioner.settings import Settings, get_loader


class TestLoader():
    '''Test the settings.get_loader function'''

    def test_yaml(self):
        '''test the yaml loader'''
        loader = get_loader('yaml')
        yml_obj = '''
  - 1
  - 2
  - 3
'''
        assert [1, 2, 3] == loader(yml_obj)

    def test_json(self):
        '''test the json loader'''
        loader = get_loader('json')
        js_obj = '''[1,2,3]'''
        assert [1, 2, 3] == loader(js_obj)

    def test_unknown(self):
        '''test unknown format error'''
        with pytest.raises(AssertionError):
            get_loader("random name")


class TestSettings():
    '''Test the settings class'''

    def test_added_settings(self):
        '''test adding of settings'''
        yml = '''
languages:
    fake_language:
        timeLimit: 20
'''
        Settings.load_added_settings(yml)
        language_settings = Settings.get_language_settings('fake_language')
        assert language_settings is not None
        assert language_settings.get('timeLimit') == 20

    def test_get(self):
        '''Test Settings.get()'''
        assert Settings.get("workspace") == "playground"
