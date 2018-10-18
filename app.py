from socket import *
import json, os
import time
from datetime import tzinfo, timedelta, datetime
import argparse
import link as lk
import handler as mh
import config as cf

import _thread

def loadConfig(**kwargs):

    config = cf.Config()

    source_conf, model_conf, store_conf = config.readModelsConfigFile(file='./model.conf')

    return source_conf, model_conf, store_conf

def workflow(id, source_conf, model_conf, store_conf, **kwargs):

    flowid = str(id)
    

    linktodata = lk.Connector(id)
    model = mh.Model(flowid)

    source_conf, model_conf, store_conf = loadConfig()
    data = linktodata. .getdata(source_conf)
    data = model.query(data, model_conf)
    link.writedata(store_conf, data)

def main():
    print("start")

    loadConfig()

    try:
        _thread.start_new(workflow(a[0]),)
        _thread.start_new(workflow(a[1],)


if __name__ == '__main__':
    main()
