# -*- coding: utf-8 -*-
"""Tutorial using all elements to define a sine wave."""

import argparse

import math
import datetime
import time

from influxdb import InfluxDBClient

USER = 'root'
PASSWORD = 'root'
DBNAME = 'db1'


def main(host='192.168.1.53', port=8086):
    """Define function to generate the sin wave."""
    #now = datetime.datetime.today()
    #result = []

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    print("Create database: " + DBNAME)
    client.create_database(DBNAME)
    client.switch_database(DBNAME)

    while 1:
        for angle in range(0, 259):
            dt = time.time()
            dt = (datetime.datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
            y = 10 + math.sin(math.radians(angle)) * 10

            point = [{
                "measurement": "raw_data",
                "time": dt,
                "fields": {
                    "sine": y
                }
            }]

            # Write points
            print(point)
            client.write_points(point)

            time.sleep(5)

            #query = 'SELECT * FROM data'
            #print("Querying data: " + query)
            #result = client.query(query, database=DBNAME)
            #print("Result: {0}".format(result))

            """
            You might want to comment the delete and plot the result on InfluxDB
            Interface. Connect on InfluxDB Interface at http://127.0.0.1:8083/
            Select the database tutorial -> Explore Data
            Then run the following query:
                SELECT * from foobar
            """

            #print("Delete database: " + DBNAME)
            #client.drop_database(DBNAME)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)