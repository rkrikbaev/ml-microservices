# -*- coding: utf-8 -*-
"""Tutorial using all elements to define a sine wave."""

import math
import datetime
import time
import _thread
import random

from scipy import signal
import numpy as np

from influxdb import InfluxDBClient

USER = 'root'
PASSWORD = 'root'
DBNAME = 'db'
host='192.168.4.33'
port=8086

now = datetime.datetime.today()

client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)


# print("Create database: " + DBNAME, "on host:", host)
# client.create_database(DBNAME)
# client.switch_database(DBNAME)

genFuncs_angle = 0
genFuncs_line = 0
genRandBinaryFlag = 0
genTimeLineFlag = 1
genTimeLineState = 1

def generateFuncs(linemaxmin, threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            # half-sinusoid and line for general testing
            global genFuncs_angle, genFuncs_line, genRandBinaryFlag, genTimeLineFlag, genTimeLineState
            genFuncs_angle += 1
            sin = math.sin(math.radians(genFuncs_angle))
            if genFuncs_angle >= 179: genFuncs_angle = 1

            if genFuncs_line < linemaxmin[0]: genFuncs_line = linemaxmin[0]
            genFuncs_line += 1
            if genFuncs_line > linemaxmin[1]: genFuncs_line = linemaxmin[0]

            json_body_lines = [
                {
                    "measurement": "meas",
                    "fields": {
                        "sinusoid": int(sin*100),
                        "sinangle": int(genFuncs_angle),
                        "stepline": int(genFuncs_line)
                    }
                }
            ]
            client.write_points(json_body_lines)

        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))

def main():

    _thread.start_new_thread(generateFuncs([10, 140], "Thread-Gen-1", 5))  # line [min,max] and rand [min,max]

if __name__ == '__main__':

    print("Started gathering statistics")

    while True:
        try:
            main()
        except Exception as e:
            print("Error: unable to start thread" + str(e))