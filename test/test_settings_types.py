import unittest
import os

from django_ini_settings.settings_types import (Setting, DictItemSetting,
                                                  BoolSetting, IntSetting)
from django_ini_settings.statics import ANY, NAME_TO_UPPER, NAME_AS_IS


class SettingTestCase(unittest.TestCase):

    def test_get_setting_name(self):
        s1 = Setting(NAME_AS_IS)
        s2 = Setting(NAME_TO_UPPER)
        s3 = Setting("setting")
        s4 = Setting(("list", "setting"))
        self.assertEqual(s1.get_setting_name("application", "test"), "test")
        self.assertEqual(s2.get_setting_name("application", "test"), "TEST")
        self.assertEqual(s3.get_setting_name("application", "test"), "setting")
        self.assertEqual(s4.get_setting_name("application", "test"), ("list", "setting"))

    def test_set_value(self):

        class Test(object):
            pass

        s1 = Setting(NAME_AS_IS)
        s1.set_value(Test, "application", "test1", "value1")
        s2 = Setting(NAME_TO_UPPER)
        s2.set_value(Test, "application", "test2", "value2")
        s3 = Setting("setting")
        s3.set_value(Test, "application", "test3", "value3")
        self.assertEqual(Test.test1, "value1")
        self.assertEqual(Test.TEST2, "value2")
        self.assertEqual(Test.setting, "value3")


class BoolSettingTestCase(unittest.TestCase):

    def test_get_value(self):
        s = BoolSetting("setting")
        self.assertEqual(s.get_value("true"), True)
        self.assertEqual(s.get_value("True"), True)
        self.assertEqual(s.get_value("TRUE"), True)
        self.assertEqual(s.get_value("false"), False)
        self.assertEqual(s.get_value("False"), False)
        self.assertEqual(s.get_value("FALSE"), False)


class IntSettingTestCase(unittest.TestCase):

    def test_get_value(self):
        s = IntSetting("setting")
        self.assertEqual(s.get_value("1"), 1)
        self.assertEqual(s.get_value("12"), 12)
        self.assertEqual(s.get_value("-12"), -12)
        self.assertRaises(ValueError, s.get_value, "-1.2")


class DictItemSettingTestCase(unittest.TestCase):

    def test_set_value(self):

        class Test(object):
            test1 = {}
            test2 = {"a": "b"}
            test3 = {"c": {"d": "e"}}
            test4 = {"c": {"d": {"e": "f"}}}


        s1 = DictItemSetting(("test1", "setting"))
        s1.set_value(Test, "application", "test1", "value1")
        s2 = DictItemSetting(("test2", "a"))
        s2.set_value(Test, "application", "test2", "value2")
        s3 = DictItemSetting(("test3", "c", "d"))
        s3.set_value(Test, "application", "test3", "value3")
        s4 = DictItemSetting(("test4", "c", "d", "e"))
        s4.set_value(Test, "application", "test4", "value4")

        self.assertEqual(Test.test1["setting"], "value1")
        self.assertEqual(Test.test2["a"], "value2")
        self.assertEqual(Test.test3["c"]["d"], "value3")
        self.assertEqual(Test.test4["c"]["d"]["e"], "value4")