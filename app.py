from socket import *
import json, os
import time
from datetime import tzinfo, timedelta, datetime

import link as lk
import handler as mh
import _thread

def loadConfig(**kwargs):

    source_conf, model_conf, store_conf = lk.Connector.getdata()

    return source_conf, model_conf, store_conf

def workflow(**kwargs):

    link = lk.Connector()
    model = mh.Model()

    source_conf, model_conf, store_conf = loadConfig()
    data = link.getdata(source_conf, model_conf, store_conf)
    data = model.query(data)
    link.writedata(store_conf, data)

def main():
    print("start")
    try:
        _thread.start_new(workflow(),)
        _thread.start_new(workflow(),)

if __name__ == '__main__':
    main()
