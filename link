#!/home/user/bin/python

from datetime import datetime
from influxdb import InfluxDBClient, DataFrameClient

header = {'Content-Type': 'application/json',\
                  'Accept': 'application/json'}



class Influxdb():

    def __init__(self, **kwargs):

        self.NodeConfig = kwargs

        self.query_body = query_body

        self.body_to_write = body_to_write

        self.measurement = measurement

        self.client = InfluxDBClient(self.host, self.port, self.user, self.password)

    def time(self):
        self.dt = datetime.now().isoformat()


    def getdata(self):


        return self

    def writedata(self):
        put_in_influx = [{
            "measurement": self.measurement,
            "tags": {"title": ""},
            "time": self.dt,
            "fields": self.body_to_write
        }]

        self.client.write_points(put_in_influx)

#class getConfig(object):
#    def __init__(self, files = "./"):
#        self.files = files                      #list of files with configuration
#    def readJsonFile(self, **kwarg):


