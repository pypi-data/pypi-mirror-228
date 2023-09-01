#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
"""
import json

from mobio.libs.Singleton import Singleton
from mobio.sdks.base.common.system_config import SystemConfig
from mobio.sdks.base.configs import ApplicationConfig

LANG_VI = 'vi'
LANG_EN = 'en'

class LangConstant:
    LANG = 'lang'
    KEYS = 'keys'
    DEFAULT = 'default'

class LangStructure:
    MESSAGE = 'message'
    CODE = 'code'
    LANG = 'lang'

class LangError:
    CUSTOM_ERROR = 'custom_error'
    BAD_REQUEST = 'bad_request'
    UNAUTHENTICATE = 'unauthentice'
    NOT_ALLOWED = 'not_allowed'
    NOT_FOUND = 'not_found'
    INTERNAL_SERVER_ERROR = 'internal_server_error'
    VALIDATE_ERROR = 'validate_error'
    LANG_NOT_SUPPORT_ERROR = 'lang_not_support_error'
    MUST_NOT_EMPTY = 'must_not_empty'
    NOT_EXIST = 'not_exist'
    ALREADY_EXIST = 'already_exist'
    MESSAGE_SUCCESS = 'message_success'
    UNAUTHORIZED = 'unauthorized'

@Singleton
class LangConfig:
    def __init__(self):
        sys_conf = SystemConfig()
        self.keys = sys_conf.get_section_map(LangConstant.LANG)[LangConstant.KEYS]
        self.default = sys_conf.get_section_map(LangConstant.LANG)[LangConstant.DEFAULT]

        self.languages = self.keys.split(',')
        self.support = {}
        for lang in self.languages:
            lang = lang.strip()
            resource = LangConfig._lang_json(lang)
            if resource:
                self.support.update({lang: resource})

    def lang_map(self, lang=None):
        if not lang:
            lang = self.default

        if lang in self.support:
            return self.support[lang]

        return self.support[self.default]

    def get(self, key, lang=None, value_if_not=None):
        if not lang:
            lang = self.default

        if lang not in self.support:
            if not value_if_not:
                return value_if_not
            return key

        result = self.support[lang].get(key, None)
        if result is None and value_if_not is not None:
            result = value_if_not
            
        return result

    @staticmethod
    def _lang_json(lang):
        path = ApplicationConfig.LANG_DIR + '/message_' + lang + '.json'
        try:
            with open(path) as data_file:
                data = json.loads(data_file.read())

            return data
        except Exception as ex:
            print(ex)
            return None
