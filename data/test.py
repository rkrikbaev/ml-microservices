#!/usr/bin/python3

import math
import datetime
import time
import _thread

from influxdb import InfluxDBClient


# Define a function for the thread
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

client = InfluxDBClient('192.168.4.33', 8086, '', '', 'db')

genFuncs_angle = 0
genFuncs_line = 0
genRandBinaryFlag = 0
genTimeLineFlag = 1
genTimeLineState = 1

def generateFuncs(linemaxmin, threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            dt = time.time()
            dt = (datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
            print(("try again at {0}".format(dt)))
            # half-sinusoid and line for general testing
            global genFuncs_angle, genFuncs_line, genRandBinaryFlag, genTimeLineFlag, genTimeLineState
            genFuncs_angle += 1
            sin = math.sin(math.radians(genFuncs_angle))
            if genFuncs_angle >= 179: genFuncs_angle = 1

            if genFuncs_line < linemaxmin[0]: genFuncs_line = linemaxmin[0]
            genFuncs_line += 1
            if genFuncs_line > linemaxmin[1]: genFuncs_line = linemaxmin[0]

            json_body_lines = [{
                    "measurement": "lines",
                    "time": dt,
                    "fields": {
                        "sinusoid": int(sin*100),
                        "sinangle": int(genFuncs_angle),
                        "stepline": int(genFuncs_line)
                    }
                }]
            client.write_points(json_body_lines)
        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))

# Create two threads as follows
try:
    #_thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    #_thread.start_new_thread( print_time, ("Thread-2", 2, ) )
    #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-1", 2 ))  # line [min,max] and rand [min,max]
    _thread.start_new_thread(generateFuncs, ([10,140], "Thread-Gen-10", 5) ) # line [min,max] and rand [min,max]
    generateFuncs([10, 140], "Thread-Gen-1", 2 )

except:
    print ("Error: unable to start thread")

while 1:
    pass
