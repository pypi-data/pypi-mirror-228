#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Company: MobioVN
"""

import datetime
from functools import wraps

from flask import request
from mobio.libs.logging import LoggingConfig, MobioLogging, LoggingConstant
from mobio.sdks.base.common import CONSTANTS
from mobio.sdks.base.common.lang_config import LangConfig, LangError, LangStructure

from mobio.sdks.base.common.system_config import SystemConfig

from mobio.sdks.base.common.utils import get_request_id


class BaseMoError(Exception):
    """ Attribute not found. """

    def __init__(self, *args):  # real signature unknown
        # *args is used to get a list of the parameters passed in
        param = None
        array = [a for a in args]
        try:
            param = request.args.get('lang')
            if len(array) > 0:
                str(array[0]).encode('utf-8')
            self.params = array
        except Exception as ex:
            print("my_except/BaseMoError.__init__", ex)
            self.params = array[1:]

        self.lang_config = LangConfig()
        self.param = param
        if not self.param:
            self.param = self.lang_config.default
        self.lang = self.lang_config.lang_map(param)
        self.message_name_default = LangError.VALIDATE_ERROR

        self.sys_conf = SystemConfig()

    def get_message(self):
        try:
            return self._get_message()
        except Exception as ex:
            print("my_except/BaseMoError.get_message", ex)
            MobioLogging().warning('%s :: %s exception occurred' %
                                           (str(datetime.datetime.now()), self.get_class_name()))
            code = self.lang[LangError.INTERNAL_SERVER_ERROR][LangStructure.CODE]
            message = self.lang[LangError.INTERNAL_SERVER_ERROR][LangStructure.MESSAGE]
            return BaseMoError.build_message_error(code, message)

    def _get_message(self):
        log_mod = self.sys_conf.get_section_map(CONSTANTS.LOGGING_MODE)

        len_arg = len(self.params)
        message_name = self.message_name_default
        if len_arg > 0:
            message_name = self.params[0]

        log_message = None
        if message_name not in self.lang:
            log_message = "arg[0] là [%s] không được định nghĩa trong file Lang" % message_name
            message_name = self.message_name_default

        code = self.lang[message_name][LangStructure.CODE]
        message = self.lang[message_name][LangStructure.MESSAGE]

        is_custom_except = message_name != LangError.INTERNAL_SERVER_ERROR and message_name != LangError.MESSAGE_SUCCESS
        mod1 = int(log_mod[LoggingConstant.LOG_FOR_ALL_CUSTOMIZE_EXCEPTION]) == 1 and is_custom_except
        mod2 = int(log_mod[LoggingConstant.WRITE_TRACEBACK_FOR_ALL_CUSTOMIZE_EXCEPTION]) == 1 and is_custom_except

        mod3 = int(log_mod[LoggingConstant.WRITE_TRACEBACK_FOR_GLOBAL_EXCEPTION]) == 1
        mod3 = mod3 and message_name == LangError.INTERNAL_SERVER_ERROR
        mod4 = int(log_mod[LoggingConstant.LOG_FOR_GLOBAL_EXCEPTION]) == 1
        mod4 = mod4 and message_name == LangError.INTERNAL_SERVER_ERROR

        mod5 = int(log_mod[LoggingConstant.LOG_FOR_REQUEST_SUCCESS]) == 1
        mod5 = mod5 and message_name == LangError.MESSAGE_SUCCESS

        if mod1 or mod2 or mod3 or mod4 or mod5:
            MobioLogging().debug('==================================================================')
            MobioLogging().debug(str(datetime.datetime.now()))
            if log_message:
                MobioLogging().debug(log_message)

        errors = None
        if len_arg > 2:
            errors = self.params[2]
        elif len_arg > 1:
            errors = self.params[1]

        try:
            if LoggingConfig.K8S != '1':  # turn off new logging style
                if mod1 or mod4 or mod5:
                    body = str(request.data, 'utf-8')
                    if body is None or body == '' or body == b'':
                        body = str(request.form)
                    MobioLogging().debug(
                        'request_id: {request_id} \n HTTP/1.1 {method} {url}\n{headers}\nClient-Ip: {client_ip}'
                        '\n\nbody: {body}'.format(
                            request_id=get_request_id(),
                            method=request.method,
                            url=request.url,
                            headers='\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
                            client_ip=request.remote_addr,
                            body=body
                        ))
            else:
                if mod1 or mod4 or mod5:
                    body = str(request.data, 'utf-8')
                    if body is None or body == '' or body == b'':
                        body = str(request.form)

                    headers = []

                    for k, v in request.headers.items():
                        headers.append({
                            k: v
                        })
                    logs = {
                        "request_id": get_request_id(),
                        "method": request.method,
                        "url": request.url,
                        "headers": headers,
                        "body": body
                    }
                    MobioLogging().info(logs, get_request_id())
        except Exception as ex:
            print("my_except/BaseMoError._get_message", ex)
            pass

        if mod2 or mod3:
            MobioLogging().exception('%s exception occurred' % self.get_class_name())

        if message and str(message).find('%s') >= 0:
            params = list(self.params[1:])
            message = message % tuple(params)
            return BaseMoError.build_message_error(code, message, self.param)
        else:
            return BaseMoError.build_message_error(code, message, self.param, errors)

    @staticmethod
    def build_message_error(code, message, lang=None, errors=None):
        if errors:
            return {
                LangStructure.CODE: code,
                LangStructure.MESSAGE: message,
                LangStructure.LANG: lang,
                'errors': errors
            }
        return {
            LangStructure.CODE: code,
            LangStructure.MESSAGE: message,
            LangStructure.LANG: lang
        }

    def get_class_name(self):
        return self.__class__.__name__


class ParamInvalidError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(ParamInvalidError, self).__init__(self, *args)
        self.message_name_default = LangError.VALIDATE_ERROR


class InputNotFoundError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(InputNotFoundError, self).__init__(self, *args)
        self.message_name_default = LangError.NOT_FOUND


class LogicSystemError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(LogicSystemError, self).__init__(self, *args)
        self.message_name_default = LangError.NOT_ALLOWED


class DBLogicError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(DBLogicError, self).__init__(self, *args)
        self.message_name_default = LangError.BAD_REQUEST


class CustomError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(CustomError, self).__init__(self, *args)
        self.message_name_default = LangError.CUSTOM_ERROR


class CustomUnauthorizeError(BaseMoError):
    def __init__(self, *args):  # real signature unknown
        super(CustomUnauthorizeError, self).__init__(self, *args)
        self.message_name_default = LangError.UNAUTHENTICATE


class UnauthorizationError(BaseMoError):
    def __init__(self, *args):
        super(UnauthorizationError, self).__init__(self, *args)
        self.message_name_default = LangError.UNAUTHORIZED

# --------------------------- TEST ---------------------------


if __name__ == '__main__':
    def _try_catch_error2(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                print('ok 2')
                return f(*args, **kwargs)
            except BaseMoError as ex:
                print('error 2 %s' % ex)

        return decorated


    def _try_catch_error1(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                print('ok 1')
                return f(*args, **kwargs)
            except BaseMoError as ex:
                print('error 1 %s' % ex.get_message())

        return decorated


    @_try_catch_error2
    @_try_catch_error1
    def __function():
        raise BaseMoError('text')


    try:
        __function()
    except Exception as e:
        print(e.args)
