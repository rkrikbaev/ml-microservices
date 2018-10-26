# -*- coding: utf-8 -*-
"""Tutorial using all elements to define a sine wave."""

import math
import datetime
import time
import _thread

from influxdb import InfluxDBClient

USER = 'admin'
PASSWORD = '12345'
DBNAME = 'db1'
host='192.168.4.33'
port=8086

client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)


print("Create database: " + DBNAME, "on host:", host)
client.create_database(DBNAME)
client.switch_database(DBNAME)

genFuncs_angle = 0
genFuncs_line = 0
genRandBinaryFlag = 0
genTimeLineFlag = 1
genTimeLineState = 1
genFuncs_line_prev = 0
genFuncs_line_cur = 0
step = 0
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

def generateFuncs(linemaxmin, threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            global step, genFuncs_line_cur, genFuncs_line_prev, genFuncs_angle, genFuncs_line, genRandBinaryFlag, genTimeLineFlag, genTimeLineState
            dt = time.time()
            dt = (datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
            # half-sinusoid and line for general testing

            genFuncs_angle += 1
            sin = math.sin(math.radians(genFuncs_angle))

            if genFuncs_angle >= 359: genFuncs_angle = 1

            genFuncs_line += 1

            if genFuncs_line < linemaxmin[0]: genFuncs_line = linemaxmin[0]

            if genFuncs_line > linemaxmin[1]: genFuncs_line = linemaxmin[0]

            genFuncs_line_cur = genFuncs_line

            if (genFuncs_line_cur - genFuncs_line_prev) > 50:

                genFuncs_line_prev = genFuncs_line_cur

            json_body_lines = [{
                "measurement": threadName,
                "time": dt,
                "fields": {
                    "sinusoid": int(sin*100),
                    "sinangle": int(genFuncs_angle),
                    "stepline": int(genFuncs_line_prev)
                }
            }]
            step += 1
            client.write_points(json_body_lines)

        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))
            client.close()
            step = 0
            #client.drop_database(DBNAME)
        finally:
            print("Интерация номер: {0}".format(step))


def main():
    print("Started gathering statistics")
    try:

        _thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-1", 1 ))  # line [min,max] and rand [min,max]
        #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-2", 1 ))  # line [min,max] and rand [min,max]
        #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-3", 1 ))  # line [min,max] and rand [min,max]
        #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-4", 1 ))  # line [min,max] and rand [min,max]
        #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-5", 1 ))  # line [min,max] and rand [min,max]
        #_thread.start_new_thread( generateFuncs, ([10, 140], "Thread-Gen-6", 1 ))  # line [min,max] and rand [min,max]

    except Exception as e:
        print("Error: unable to start thread " + str(e))

    while 1:
        time.sleep(1)
        print(time.time())
        pass

if __name__ == '__main__':
    main()