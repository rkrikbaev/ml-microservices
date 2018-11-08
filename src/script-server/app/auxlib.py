#! /usr/bin/python3
"""
Дополнительная библиотека модулей не участвующая в работе основного workflow
"""

import json, time, datetime

class DateTime(object):
    def __init__(self):
        pass
    def utc_time(self):                                #получение времени в формате UTC
        dt = time.time()
        dt = datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')
        return dt
