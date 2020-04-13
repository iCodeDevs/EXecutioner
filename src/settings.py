'''
Load and hold the settings for compile,execute and evaluate steps
'''
import os
import inspect
import json
SETTINGS = {}

def combine_settings(main_settings, added_settings):
    ''' combine 2 dict/list objects in depth '''
    if not isinstance(added_settings, type(main_settings)):
        raise Exception("incompatible types")
    if isinstance(main_settings, dict):
        common_keys = set(main_settings.keys()) & set(added_settings.keys())
        for key in common_keys:
            if isinstance(main_settings[key], (str, int, float)):
                main_settings[key] = added_settings[key]
            else:
                combine_settings(main_settings[key], added_settings[key])
    elif isinstance(main_settings, list):
        main_settings.extend(added_settings)
    return main_settings


def load_default_settings():
    ''' loads the default settings '''
    file_loc = inspect.getfile(inspect.currentframe())
    module_folder = os.path.dirname(file_loc)
    settings_file = os.path.join(module_folder, "."+os.path.sep+"settings.json")
    return json.load(open(settings_file, 'r'))

def load_added_settings(file_obj):
    ''' load extra settings '''
    added_settings = json.load(file_obj)
    return combine_settings(SETTINGS, added_settings)

SETTINGS = load_default_settings()
