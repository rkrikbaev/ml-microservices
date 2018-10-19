# -*- coding: utf-8 -*-
"""Tutorial using all elements to define a sine wave."""

import math
import datetime
import time
import _thread
import random

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


def generateFuncs(linemaxmin, rand, threadName, delay):
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
                    "measurement": "lines",
                    "fields": {
                        "sinusoid": int(sin*100),
                        "sinangle": int(genFuncs_angle),
                        "stepline": int(genFuncs_line)
                    }
                }
            ]
            client.write_points(json_body_lines)

            # general random generation, for usage in Timeline and others
            rand1 = random.randint(rand[0], rand[1])
            rand2 = random.randint(rand[0]*10, rand[1]*10)

            _randbin = random.randint(1, 300)
            randbin = 1
            if _randbin >= 299:
                genRandBinaryFlag = random.randint(20,40)

            # will generate series 20-40 of zeros, after triggering
            if genRandBinaryFlag > 0:
                randbin = 0
                genRandBinaryFlag -= 1


            if genTimeLineFlag > 0:
                genTimeLineFlag  -= 1
            else:
                genTimeLineState = random.randint(1, 4)
                genTimeLineFlag = random.randint(5, 50)

            json_body_random = [
                {
                    "measurement": "randomNumbers",
                    "fields": {
                        "rand": int(rand1),
                        "randX10": int(rand2),
                        "randbinary": int(randbin),
                        "timeline": int(genTimeLineState)
                    }
                }
            ]
            client.write_points(json_body_random)

            # generate event text for PX-timeseries
            rand3 = random.randint(1,400)
            if rand3 >= 399: # eg 0.25 % prob
                eventString = "color:blue,icon:px-fea:asset,text:Обычное событие"
                rand4a = random.randint(1, 100)
                print ("%d rand4a" % rand4a)
                if rand4a >= 90:
                    eventString = "color:orange,icon:px-fea:deployments,text:Уникальное событие"
                    print ("we have UNIQ event %s" % eventString)
                elif rand4a >= 70:
                    eventString = "color:green,icon:px-fea:administration,text:Редкое событие"
                    print ("We have RARE event %s" % eventString)

                json_body_event = [
                    {
                        "measurement": "timeSeriesEvent",
                        "fields": {
                            "eventInfo": str("%s" % (eventString))
                        }
                    }
                ]
                client.write_points(json_body_event)

        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))



def sinus(threadName, delay):
    """Define function to generate the sin wave."""
    time.sleep(delay)
    while 1:
        try:
            for angle in range(0, 360):
                y = 10 + math.sin(math.radians(angle)) * 10

                dt = int(now.strftime('%s')) + angle
                dt = (datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
                point = [{
                    "measurement": 'gen',
                    "time": dt,
                    "fields": {
                        "value": y
                    }
                }]

                # Write points
                client.write_points(point)


                query = 'SELECT * FROM '+DBNAME+'.autogen.meas WHERE time > now() - 1m ORDER BY time DESC LIMIT 1'
                #print("Querying data: " + query)
                result = client.query(query, database=DBNAME)
                #print("Recieve result: {0}".format(result))

                """
                You might want to comment the delete and plot the result on InfluxDB
                Interface. Connect on InfluxDB Interface at http://127.0.0.1:8083/
                Select the database tutorial -> Explore Data
                Then run the following query:
                    SELECT * from foobar
                """
        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))


def main():

    _thread.start_new_thread(generateFuncs,([10, 140], [0, 5], "Thread-Gen-1", 5))  # line [min,max] and rand [min,max]

if __name__ == '__main__':

    print("Started gathering statistics")

    while True:
        try:
            main()
        except Exception as e:
            print("Error: unable to start thread" + str(e))
        finally:
            print("over")
            client.close()