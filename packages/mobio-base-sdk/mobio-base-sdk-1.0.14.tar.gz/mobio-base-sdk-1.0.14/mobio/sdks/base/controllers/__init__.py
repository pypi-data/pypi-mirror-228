#!/usr/bin/python
# -*- coding: utf8 -*-
from flask import request

from mobio.libs.validator import HttpValidator, VALIDATION_RESULT
from mobio.sdks.base.common.lang_config import LangError, LangConfig, LANG_VI
from mobio.sdks.base.common.mobio_exception import ParamInvalidError


class BaseController(object):
    PARAM_INVALID_VALUE = 412

    @staticmethod
    def abort_if_validate_error(rules, data):
        valid = HttpValidator(rules)
        val_result = valid.validate_object(data)
        if not val_result[VALIDATION_RESULT.VALID]:
            errors = val_result[VALIDATION_RESULT.ERRORS]
            raise ParamInvalidError(LangError.VALIDATE_ERROR, errors)

    @staticmethod
    def validate_optional_err(rules, data):
        valid = HttpValidator(rules)
        val_result = valid.validate_optional(data)
        if not val_result[VALIDATION_RESULT.VALID]:
            errors = val_result[VALIDATION_RESULT.ERRORS]
            raise ParamInvalidError(LangError.VALIDATE_ERROR, errors)

    @staticmethod
    def abort_if_param_empty_error(param, param_name):
        if param is None or param is '':
            raise ParamInvalidError(LangError.MUST_NOT_EMPTY, param_name)

    def __init__(self):
        try:
            param = request.args.get('lang', LANG_VI)
            if param and param not in LangConfig().languages:
                raise ParamInvalidError(LangError.LANG_NOT_SUPPORT_ERROR)
            self.lang = LangConfig().lang_map(param)
        except:
            param = None
        self.language = param or LANG_VI
