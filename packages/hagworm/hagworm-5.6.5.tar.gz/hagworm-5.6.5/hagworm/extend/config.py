# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import dataclasses

from configparser import RawConfigParser

from .base import Utils


class HostType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        host, port = val.split(r':', 2)
        return host.strip(), int(port.strip())


class JsonType(str):

    @classmethod
    def decode(cls, val):

        if not val:
            return None

        return Utils.json_decode(val)


class StrListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_str(val)


class IntListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_int(val)


class FloatListType(str):

    @classmethod
    def decode(cls, val):
        return Utils.split_float(val)


class Field:

    __slots__ = [r'section']

    def __init__(self, section):

        self.section = section


class ConfigureMetaclass(type):
    """配置类元类，增加dataclass修饰
    """

    def __new__(mcs, name, bases, attrs):
        return dataclasses.dataclass(init=False)(
            type.__new__(mcs, name, bases, attrs)
        )


class ConfigureBase(metaclass=ConfigureMetaclass):
    """配置类
    """

    __slots__ = [r'_parser', r'_key_section']

    def __init__(self):

        super().__init__()

        self._parser = RawConfigParser()

        self._key_section = {
            f'{_field.default.section}/{_key}': (_key, _field.default.section, _field.type,)
            for _key, _field in self.__dataclass_fields__.items()
        }

    def _load_options(self):

        for _key, _section, _type in self._key_section.values():

            # 优先处理环境变量
            _env_key = f'{_section}_{_key}'.upper()
            _env_val = os.getenv(_env_key, None)

            if _env_val is not None:
                self._parser.set(_section, _key, _env_val)
                Utils.log.info(f'load environment variable {_env_key}: {_env_val}')

            if _type is str:
                self.__setattr__(_key, self._parser.get(_section, _key))
            elif _type is int:
                self.__setattr__(_key, self._parser.getint(_section, _key))
            elif _type is float:
                self.__setattr__(_key, self._parser.getfloat(_section, _key))
            elif _type is bool:
                self.__setattr__(_key, self._parser.getboolean(_section, _key))
            else:
                self.__setattr__(_key, _type.decode(self._parser.get(_section, _key)))


class Configure(ConfigureBase):
    """配置类
    """

    def get_option(self, section, option):

        return self._parser.get(section, option)

    def get_options(self, section):

        parser = self._parser

        options = {}

        for option in parser.options(section):
            options[option] = parser.get(section, option)

        return options

    def set_options(self, section, **options):

        if not self._parser.has_section(section):
            self._parser.add_section(section)

        for option, value in options.items():
            self._parser.set(section, option, value)

        self._load_options()

    def read(self, path):

        self._parser.clear()
        self._parser.read(path, r'utf-8')

        self._load_options()

    def read_str(self, val):

        self._parser.clear()
        self._parser.read_string(val)

        self._load_options()

    def read_dict(self, val):

        self._parser.clear()
        self._parser.read_dict(val)

        self._load_options()
