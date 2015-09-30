import unittest
import os

from django_ini_settings.settings_types import (DictItemSetting, StringSetting,
                                           BoolSetting, IntSetting)
from django_ini_settings.load import match_setting, load_ini
from django_ini_settings.statics import ANY, NAME_TO_UPPER


class MatchSettingTestCase(unittest.TestCase):
    config_mapping = {
        ("urls", "media_url"): StringSetting("MEDIA_URL"),
        ("urls", "static_url"): StringSetting("STATIC_URL"),
        ("application", "max_file_size"): IntSetting("MAX_FILE_SIZE"),
        ("application", ANY): StringSetting(NAME_TO_UPPER)
    }

    def test_option_exists(self):
        self.assertEqual(
            self.config_mapping[("application", "max_file_size")],
            match_setting("application", "max_file_size", self.config_mapping)
        )

    def test_option_not_exists(self):
        self.assertEqual(
            self.config_mapping[("application", ANY)],
            match_setting("application", "min_file_size", self.config_mapping)
        )

    def test_option_not_exists_no_any(self):
        self.assertIsNone(
            match_setting("urls", "another_url", self.config_mapping)
        )

    def test_section_not_exists(self):
        self.assertIsNone(
            match_setting("nothere", "another_url", self.config_mapping)
        )


class LoadIniTestCase(unittest.TestCase):
    """
    test_1.ini
    [database]
    user = postgres
    password = apass

    [string]
    a_string = a value
    another = /static/url

    [security]
    secret_key = krhnfgjn34rfm3iof4!JIKMK
    debug = false

    [bool]
    abool = True
    bbool = False
    cbool = true
    dbool = false

    [int]
    test = 13

    [application]
    max_file_size = 234
    another_setting = test setting
    """
    config_mapping = {
        ("urls", "media_url"): StringSetting("MEDIA_URL"),
        ("urls", "static_url"): StringSetting("STATIC_URL"),
        ("application", "max_file_size"): IntSetting("MAX_FILE_SIZE"),
        ("application", ANY): StringSetting(NAME_TO_UPPER)
    }

    def test_default_config(self):

        class Test(object):

            DATABASES = {
                'default': {
                    'ENGINE': 'django.contrib.gis.db.backends.postgis',
                    'NAME': 'cas',
                    'USER': 'root',
                    'PASSWORD': 'password',
                    'HOST': '',
                    'PORT': ''
                }
            }

        load_ini(
            ini_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_1.ini'),
            settings_module=Test
        )

        self.assertEqual(Test.DATABASES["default"]["USER"], "postgres")
        self.assertEqual(Test.DATABASES["default"]["PASSWORD"], "apass")
        self.assertEqual(Test.A_STRING, "a value")
        self.assertEqual(Test.ANOTHER, "/static/url")
        self.assertEqual(Test.SECRET_KEY, "krhnfgjn34rfm3iof4!JIKMK")
        self.assertEqual(Test.DEBUG, False)
        self.assertEqual(Test.ABOOL, True)
        self.assertEqual(Test.BBOOL, False)
        self.assertEqual(Test.CBOOL, True)
        self.assertEqual(Test.DBOOL, False)
        self.assertEqual(Test.TEST, 13)
        self.assertFalse(hasattr(Test, "MAX_FILE_SIZE"))
        self.assertFalse(hasattr(Test, "ANOTHER_SETTING"))

    def test_custom_config(self):

        class Test(object):

            DATABASES = {
                'default': {
                    'ENGINE': 'django.contrib.gis.db.backends.postgis',
                    'NAME': 'cas',
                    'USER': 'root',
                    'PASSWORD': 'password',
                    'HOST': '',
                    'PORT': ''
                }
            }

        load_ini(
            ini_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_1.ini'),
            settings_module=Test,
            config_mapping=self.config_mapping
        )

        self.assertEqual(Test.DATABASES["default"]["USER"], "root")
        self.assertEqual(Test.DATABASES["default"]["PASSWORD"], "password")
        self.assertFalse(hasattr(Test, "A_STRING"))
        self.assertFalse(hasattr(Test, "ANOTHER"))
        self.assertFalse(hasattr(Test, "SECRET_KEY"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertFalse(hasattr(Test, "DEBUG"))
        self.assertEqual(Test.MAX_FILE_SIZE, 234)
        self.assertEqual(Test.ANOTHER_SETTING, "test setting")
