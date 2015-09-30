"""Definition of the types allowed in configs and methods to convert them to python"""
from statics import NAME_AS_IS, NAME_TO_UPPER


class Setting(object):
    def __init__(self, setting_name):
        self.setting_name = setting_name

    def get_setting_name(self, section, option):
        if self.setting_name == NAME_TO_UPPER:
            return option.upper()
        elif self.setting_name == NAME_AS_IS:
            return option
        return self.setting_name

    def get_value(self, conf_value):
        return conf_value

    def set_value(self, settings_module, section, option, conf_value):
        setattr(
            settings_module,
            self.get_setting_name(section, option),
            self.get_value(conf_value)
        )


class StringSetting(Setting):
    pass


class BoolSetting(Setting):

    def get_value(self, conf_value):
        return conf_value.lower() == "true"


class IntSetting(Setting):

    def get_value(self, conf_value):
        return int(conf_value)


class DictItemSetting(Setting):

    def set_value(self, settings_module, section, option, conf_value):
        dict_item = self.get_setting_name(section, option)

        dict_setting = getattr(settings_module, dict_item[0])
        for key in dict_item[1:-1]:
            dict_setting = dict_setting.setdefault(key, {})
        dict_setting[dict_item[-1]] = self.get_value(conf_value)