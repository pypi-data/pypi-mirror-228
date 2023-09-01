#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 13/02/2023
"""
import hashlib
from datetime import datetime

from flask import request


def get_request_id():
    url = request.url
    request_time = datetime.utcnow()
    identify = url + str(request_time)
    identify = identify.encode('utf-8')
    return hashlib.md5(identify).hexdigest()