# -*- coding: utf-8 -*-
"""Tutorial using all elements to define a sine wave."""

import argparse

import math
import datetime
import time


from influxdb import InfluxDBClient

USER = 'root'
PASSWORD = 'root'
DBNAME = 'db'

def main(host='192.168.4.33', port=8086):
    """Define function to generate the sin wave."""
    now = datetime.datetime.today()
    points = []
    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    #print("Create database: " + DBNAME, "on host:", host)
    #client.create_database(DBNAME)
    #client.switch_database(DBNAME)

    for angle in range(0, 360):
        y = 10 + math.sin(math.radians(angle)) * 100

        dt = int(now.strftime('%s')) + angle
        dt = (datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
        point = [{
            "measurement": 'meas',
            "time": dt,
            "fields": {
                "value": y
            }
        }]
        #points.append(point)
        print("send", dt, y)


        #print("Create database: " + DBNAME)
        #client.create_database(DBNAME)
        #client.switch_database(DBNAME)

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

        #print("Delete database: " + DBNAME)
        #client.drop_database(DBNAME)
        time.sleep(1)


if __name__ == '__main__':

    while True:
        try:
            main()
        except:
            print("Error")
