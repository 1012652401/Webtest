#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import ConfigParser


def get_cur_path():
    path = os.path.abspath(__file__+'/../..')
    return path


class Config(ConfigParser.ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class GetConfig(object):

    def __init__(self, path="web_info.cfg"):
        self.path = os.path.join(get_cur_path(), "conf", path)
        self.config = Config()
        self.config.read(self.path)

    def get_item(self, section, key):
        return self.config.get(section, key)

    def get_section(self):
        return self.config.sections()

    def get_options(self, section):
        return self.config.options(section)

    def get_items(self, section):
        return self.config.items(section)

