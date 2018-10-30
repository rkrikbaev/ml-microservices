#!/user/bin/python3

from socket import *
import json, os
import time
from datetime import tzinfo, timedelta, datetime
import argparse

from baselib_com import Config, LinkData, Flow

import _thread

def workflow(**kwargs):
    source_info = kwargs['source_info'][id]
    model_info = kwargs['model_info'][id]
    store_info = kwargs['store_info'][id]
    delay = kwargs['delay'][id]
    threadName = kwargs['threadName'][id]
    while 1:
        time.sleep(delay)
        try:
            source_data = LinkData.getdata(source_info)
            model_data = Flow.execute(source_data, model_info)
            store_data = LinkData.writedata(model_data, store_info)
        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))
    return source_data, model_data, store_data

def main():

    print("start")

    source_conf, model_conf, store_conf = Config().loadInfo(file='./config.conf')

    try:
        _thread.start_new(workflow(source_conf[0]),)
        _thread.start_new(workflow(source_conf[1]),)
    except Exception as e:
        print(e)

if __name__ == '__main__':
            main()


















