"""Load settings from a file to insert into your django settings.py"""
import ConfigParser
import os

from statics import ANY, NAME_TO_UPPER
from settings_types import (DictItemSetting, StringSetting,
                            BoolSetting, IntSetting)


CONFIG_FILE_MAPPING = {
    ("database", "user"): DictItemSetting(("DATABASES", "default", "USER")),
    ("database", "password"): DictItemSetting(("DATABASES", "default", "PASSWORD")),
    ("database", "engine"): DictItemSetting(("DATABASES", "default", "ENGINE")),
    ("database", "name"): DictItemSetting(("DATABASES", "default", "NAME")),
    ("database", "host"): DictItemSetting(("DATABASES", "default", "HOST")),
    ("database", "port"): DictItemSetting(("DATABASES", "default", "PORT")),
    ("security", "secret_key"): StringSetting("SECRET_KEY"),
    ("security", "debug"): BoolSetting("DEBUG"),
    ("urls", "media_url"): StringSetting("MEDIA_URL"),
    ("urls", "static_url"): StringSetting("STATIC_URL"),
    ("string", ANY): StringSetting(NAME_TO_UPPER),
    ("bool", ANY): BoolSetting(NAME_TO_UPPER),
    ("dict_item", ANY): DictItemSetting(NAME_TO_UPPER),
    ("int", ANY): IntSetting(NAME_TO_UPPER),
}


def match_setting(section, option, config_mapping):
    """Find a setting in the config mapping based of the section and option in the
    config.
    First search for the exact match of section+option. Then look for section+ANY.
    """
    if (section, option) in config_mapping:
        # Exact match
        return config_mapping[(section, option)]
    elif (section, ANY) in config_mapping:
        # Match section with any option
        return config_mapping[(section, ANY)]
    return None


def load_ini(ini_file=None, settings_module=None, config_mapping=None):
    """
    Load an ini file into your django settings.py

    To use, put something like the following in your settings module:
    from django_ini_settings.load import load_ini

    load_ini(ini_file="/etc/application/application.ini",
                      settings_module=sys.modules[__name__])

    If you want to customise the mappings from the ini to your settings then,
    you can do something like this:
    from django_ini_settings.load import load_ini
    from django_ini_settings.settings_types import (DictItemSetting, StringSetting,
                                               BoolSetting, IntSetting)
    from django_ini_settings.statics import ANY, NAME_TO_UPPER

    CONFIG_FILE_MAPPING = {
        ("database", "user"): DictItemSetting(("DATABASES", "default", "USER")),
        ("database", "password"): DictItemSetting(("DATABASES", "default", "PASSWORD")),
        ("database", "engine"): DictItemSetting(("DATABASES", "default", "ENGINE")),
        ("database", "name"): DictItemSetting(("DATABASES", "default", "NAME")),
        ("database", "host"): DictItemSetting(("DATABASES", "default", "HOST")),
        ("database", "port"): DictItemSetting(("DATABASES", "default", "PORT")),
        ("security", "secret_key"): StringSetting("SECRET_KEY"),
        ("security", "debug"): BoolSetting("DEBUG"),
        ("urls", "media_url"): StringSetting("MEDIA_URL"),
        ("urls", "static_url"): StringSetting("STATIC_URL"),
        ("application", "max_file_size"): IntSetting("MAX_FILE_SIZE"),
        ("application", ANY): StringSetting(NAME_TO_UPPER),
    }

    load_ini(ini_file="/etc/application/application.ini",
                      settings_module=sys.modules[__name__],
                      config_mapping=CONFIG_FILE_MAPPING)

    """
    if config_mapping is None:
        config_mapping = CONFIG_FILE_MAPPING

    if ini_file is None:
        if os.getenv("DJANGO_CONFIG_FILE", ""):
            ini_file = os.getenv("DJANGO_CONFIG_FILE")
        else:
            raise Exception("No ini file provided, can't load settings.")

    if settings_module is None:
        raise Exception("Can't find the settings module")

    config = ConfigParser.ConfigParser()
    read_files = config.read(ini_file)

    if len(read_files) > 0:
        for section in config.sections():
            for option in config.options(section):
                setting = match_setting(section, option, config_mapping)
                if setting is None:
                    # There were no matches
                    continue
                value = config.get(section, option)
                setting.set_value(settings_module, section, option, value)