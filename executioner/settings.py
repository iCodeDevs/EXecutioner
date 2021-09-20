'''
Load and hold the settings for compile,execute and evaluate steps
'''
import os
import inspect
from typing import Any, Callable, Union, IO
import json
from deepmerge import Merger
import yaml

SETTINGS_MERGER = Merger(
    # pass in a list of tuple, with the
    # strategies you are looking to apply
    # to each type.
    [
        (list, ["append"]),
        (dict, ["merge"])
    ],
    # next, choose the fallback strategies,
    # applied to all other types:
    ["override"],
    # finally, choose the strategies in
    # the case where the types conflict:
    ["override"]
)

# ignoring R1710 because pylint not recognizing assert False as an ending


def get_loader(form='yaml') -> Callable[[IO[Union[str, bytes]]], Any]:  # pylint: disable=R1710
    '''Return load function for required format'''

    if form == 'yaml':
        return yaml.safe_load
    elif form == 'json':
        return json.loads
    assert False, f"unknown format {form}"


class Settings():
    """ Represent the settings"""

    __SETTINGS = dict()

    def __init__(self) -> None:
        '''Does not allow initialization'''
        raise NotImplementedError

    @staticmethod
    def combine_settings(main_settings, added_settings):
        '''combine 2 dict/list objects in depth'''
        assert isinstance(added_settings, type(
            main_settings)), f"incompatible types:{type(added_settings)},{type(main_settings)}"

        return SETTINGS_MERGER.merge(main_settings, added_settings)

    @staticmethod
    def load_default_settings():
        '''loads the default settings'''
        loader = get_loader()
        file_loc = inspect.getfile(inspect.currentframe())
        module_folder = os.path.dirname(file_loc)
        settings_file = os.path.join(
            module_folder, "."+os.path.sep+"settings.yaml")
        Settings.__SETTINGS = loader(open(settings_file, 'r'))

    @staticmethod
    def load_added_settings(data: str, form='yaml'):
        '''load extra settings'''
        loader = get_loader(form)
        added_settings = loader(data)
        Settings.__SETTINGS = Settings.combine_settings(
            Settings.__SETTINGS, added_settings)

    # SETTINGS based utilities
    # @staticmethod
    # def get_language(file_location):
    #     '''Identify the language of a compiled file'''
    #     extension = file_location[file_location.rindex('.')+1:]
    #     for language, lang_data in Settings.__SETTINGS.get('languages', dict()).items():
    #         if lang_data.get('compiledExtension', 0) == extension:
    #             return language
    #     return None

    @staticmethod
    def get_language_settings(language):
        '''returns the settings for given language'''
        return Settings.__SETTINGS['languages'][language]

    @staticmethod
    def get_workspace():
        '''returns the settings for given language'''
        return Settings.__SETTINGS.get("workspace", ".")

    @staticmethod
    def get(key, alt=None):
        '''returns the settings denoted by key'''
        return Settings.__SETTINGS.get(key, alt)


Settings.load_default_settings()
