#!/user/bin/python3

from socket import *
import json, os
import time
from datetime import tzinfo, timedelta, datetime
import argparse

from baselib_com import Config, LinkData, Flow

import _thread

def download_info(**kwargs):
    pass

def workflow(**kwargs):
    source_info = kwargs['source_info']
    model_info = kwargs['model_info']
    store_info = kwargs['store_info']
    source_data = LinkData.getdata(source_info)
    model_data = Flow.execute(source_data, model_info)
    store_data = LinkData.writedata(model_data, store_info)
    return source_data, model_data, store_data

def main():

    print("start")
    a = Config()
    source_conf, model_conf, store_conf = a.getInfo(file='./config.conf')
    print(source_conf, model_conf, store_conf)

    try:
        _thread.start_new(workflow(a[0]),)
        _thread.start_new(workflow(a[1]),)
    except Exception as e:
        print(e)

if __name__ == '__main__':
            main()


















