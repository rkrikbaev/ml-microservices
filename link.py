#!/home/user/bin/python

from datetime import datetime
from influxdb import InfluxDBClient, DataFrameClient

header = {'Content-Type': 'application/json',\
                  'Accept': 'application/json'}

source_conf = {"database": "raw_data",
                   "measurement": "unit1",
                   "raw_data": "pcd",
                   "orderby": "time DESC LIMIT 1",
                   "groupby": "time(1s)",
                   "query":"query = 'SELECT pcd FROM db.autogen.meas WHERE time > now() - 1m ORDER BY time DESC LIMIT 1'"
      }

class Connector():

    def __init__(self, host, port, **kwargs):

        self.host = host
        self.port = port

        self.client = InfluxDBClient(**kwargs)

    def time(self):
        self.dt = datetime.now().isoformat()

        return None

    def getdata(self,  source_conf, **kwargs):

        data = dict(source_conf)

        self.result = self.client.query(**kwargs)

        print(self.result)

        #def writedata(self):
        #    put_in_influx = [{
        #        "measurement": self.measurement,
        #        "tags": {"title": ""},
        #        "time": self.dt,
        #        "fields": self.body_to_write
        #    }]

        #   self.client.write_points(put_in_influx)

a = Connector(host='192.168.4.33', port=8086)

a.getdata(source_conf)
