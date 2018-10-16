from socket import *
import json, os
import time
from datetime import tzinfo, timedelta, datetime

import link as fx

listofnodes = {"influxdb","flask-core", "tf-core"}

class Config(object):

    def __init__(self, **kwargs):
        self.file = kwargs

    def readNodeConfigFile(self, nodename='', file=''):

        with open(file, 'r') as fp:
            listofnodes = json.load(fp)

        for item in listofnodes:
            if nodename == item:
                return listofnodes[item]

    def readModelsConfigFile(self, file=''):

        with open(file, 'r') as fp:
            listofmodels = json.load(fp)



ConfigString = Config()
InfluxNodeConfig = ConfigString.readNodeConfigFile(nodename='influxdb', file='./node.cnfg')
print(InfluxNodeConfig)
InfluxNodeConfig = ConfigString.readModelsConfigFile(file='./node.cnfg')
print(InfluxNodeConfig)
"""

def readData(self):

    countofattemts =0
    addr = (self.opcserverIP, self.opcserverPort)

    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect(addr)

    while self.opcHostConnectionOk == False & countofattemts < 10:
        action = "connect"

        data = '{"id":1,"operation":"' + action + '","item":"' + self.opcservername + '"}'                            #data = '{"id":1, "operation":"connect", "item":"Matrikon.OPC.Simulation.1"}'

        #data = str.encode(data)
        data = data.encode('utf8')

        tcp_socket.send(data)

        data = tcp_socket.recv(2048)

        data = data.decode("utf-8")
        data = json.loads(data)

        if (data['error'] == 'none'):
            if (data["operation"] == "connect"):
                self.state = "Driver connected to the host where OPC server works"
                self.opcHostConnectionOk = True
                print("Connected")
        else:
            print("Connection Error. I'm trying again and again to that host")
            countofattemts = countofattemts+1
            time.sleep(10)

    if countofattemts > 6:
        print("Connection lost, try again after 1 minute")
        time.sleep(60)

    while self.opcHostConnectionOk == True:
        print("step2.2.1 Start read opc tags")
        action = "read"
        taglist = (self.tags)
        print(taglist)

        data = '{"id":2,"operation":"' + action + '","items":' + str(taglist) + '}'                                   # data = '{"id":2,"operation":"read","items":{"U2_Program_Fuel_H012_290_AN_Ngp":""}}'
        print("step2.2.2 Send read req",data)
        data = str.encode(data)
        tcp_socket.send(data)
        print("step2.2.3 Send read req",data)
        data = tcp_socket.recv(2048)
        print("step2.2.4.0 Recv answ on req", data)
        data = data.decode("utf-8")
        print("step2.2.4.1 Recv answ on req", data)
        data = json.loads(data)
        #print("step2.2.5 Recv answ on req", data)
        if (data['error'] != 'none'):
            self.state = data['error']
            print("step2.3.1 error read opc tags:", self.state)
            self.opcConnectionOk = False
            break
        else:
            data = data["items"]
            self.datarray = data
            self.opcConnectionOk = True

        dbhostIP = self.databaseIP
        dbhosPort = self.databasePort
        measurement = self.opcservername

        client = fx.DataFrameClient()
        a = fx.Influx(self.opcserverIP, self.opcserverPort)
        b = a.get_data_as_df()
        c = a.write_data()

        #client = fx.InfluxDBClient(dbhostIP, dbhosPort, self.dbName)
        #client = InfluxDBClient(dbhostIP, dbhosPort, 'admin', '12345', self.dbName)
        #client.create_database(self.dbName)

        dt1 = datetime.now()
        dt = dt1.isoformat()

        print("step2.5", dt)

        dict_with_ints = dict((k, float(v)) for k, v in data.items())
        print("step2.5.1", dict_with_ints)

        try:

            b.write_points()
            #client.write_points(put_in_influx)

        except Exception as e:
            print(e)
            client.close()

        time.sleep(1)

nodes_addr_space = {"ip": "127.0.0.1", "port": 8086, "user": "user", "password": "pass"}
data_addr_space = {"db": "model_space", "measurement": "ARIMA"}
data_space = {"timestamp": "", "tagname": "tt01", "value": 100}

d = ConnectTo(nodes_addr_space, data_addr_space, data_space) """

def main():pass

if __name__ == '__main__':
    main()
