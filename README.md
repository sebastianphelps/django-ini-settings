# django-local-settings


This library aims to be a non-intrusive configurable way of moving some local
settings out of the django settings.py and into a deployable .ini file

## Quick-start

Install this library

    pip install django-local-settings

Add the hook into your settings.py, if you want to use the default config
mapping the following would do:

    from django_local_settings.load import load_ini

    load_ini_settings(ini_file="/etc/application/application.ini",
                      settings_module=sys.modules[__name__])

This implies that your ini file is located in /etc/application/application.ini
For example this ini might look like:

    [database]
    user = postgres
    password = secret

    [security]
    secret_key = !sfgr42325asdasd$34324
    debug = false

To insert custom configs you can either use the default format of the type as the group
and the config name as the option. e.g.

    [string]
    custom_url = /custom/url

    [bool]
    feature_on = false

    [int]
    max_num_files = 120

This would be transformed to the following in your settings.py

    CUSTOM_URL = "/custom/url"
    FEATURE_ON = False
    MAX_NUM_FILES = 120

You can also provide your own mapping, including wildcards. e.g. add the
following in your settings


    from django_local_settings.load import load_ini
    from django_local_settings.settings_types import (DictItemSetting, StringSetting,
                                               BoolSetting, IntSetting)
    from django_local_settings.statics import ANY, NAME_TO_UPPER

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

    load_ini_settings(ini_file="/etc/application/application.ini",
                      settings_module=sys.modules[__name__],
                      config_mapping=CONFIG_FILE_MAPPING)

## Environment Variables

Instead of doing:

    load_ini_settings(ini_file="/etc/application/application.ini",
                      settings_module=sys.modules[__name__])

You can also set an environment variable "DJANGO_CONFIG_FILE" containing the location of
the INI file. e.g.

    DJANGO_CONFIG_FILE=/etc/application/application.ini

Then change the line to:

    load_ini_settings(settings_module=sys.modules[__name__])

## Tests

To run the tests, first make sure you have nose. If not then:

    pip install nose

If you have nose installed then from the same directory as this README:

    nosetests

