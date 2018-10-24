from socket import *
import json
import time
from influxdb import InfluxDBClient
from datetime import tzinfo, timedelta, datetime

class ConnectTo(object):

    def __init__(self):
        self.state = ""
        self.action = ""
        self.tags = {}
        self.prop = {}
        self.operation = ""
        self.opcservername = ""
        self.datarray ={}
        self.opcConnectionOk = False
        self.opcHostConnectionOk = False

        #self.listtagsfilePath = self.workPath + listofTagsFilename

    def readConfig(self, workpath, confFileName, tagsFileName):

        confFile = workpath+confFileName
        tagsFile = workpath+tagsFileName

        items = [line.rstrip('\n') for line in open(confFile)]

        for item in items:

            props = str(item).split("=")

            for prop in props:

                if prop == "opcservername":
                    self.opcservername = props[1]
                if prop == "opcserverIP":
                    self.opcserverIP = props[1]
                if prop == "opcserverPort":
                    self.opcserverPort = int(props[1])
                if prop == "databaseIP":
                    self.databaseIP = props[1]
                if prop == "databasePort":
                    self.databasePort = int(props[1])
                if prop == "dbname":
                    self.dbName = props[1]
        print("step1.1", self.opcservername, self.opcserverIP, self.opcserverPort)

        items = [line.rstrip('\n') for line in open(tagsFile)]

        for item in items:
            self.tags[item] = ""

        self.tags = str(self.tags).replace("'",'"')

        print("step1.2. Over reading of the configuration")

    def readData(self):

        countofattemts =0
        addr = (self.opcserverIP, self.opcserverPort)
        print("setp2.0.0", addr)
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.connect(addr)
        print("setp2.0.1", countofattemts)
        while self.opcHostConnectionOk == False & countofattemts < 10:
            action = "connect"

            data = '{"id":1,"operation":"' + action + '","item":"' + self.opcservername + '"}'                            #data = '{"id":1, "operation":"connect", "item":"Matrikon.OPC.Simulation.1"}'
            print("setp2.0.2", data)
            #data = str.encode(data)
            data = data.encode('utf8')
            print("setp2.0.3", data)
            tcp_socket.send(data)
            print("setp2.0.4", data)
            data = tcp_socket.recv(2048)
            print("setp2.0.5", data)
            data = data.decode("utf-8")
            data = json.loads(data)
            print("setp2.0.6", data)
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

            client = InfluxDBClient(dbhostIP, dbhosPort, 'admin', '12345', self.dbName)
            #client.create_database(self.dbName)

            dt1 = datetime.now()
            dt = dt1.isoformat()

            print("step2.5", dt)

            dict_with_ints = dict((k, float(v)) for k, v in data.items())
            print("step2.5.1", dict_with_ints)

            try:
                put_in_influx = [{
                    "measurement": measurement,
                    "tags": {"region": "cs"},
                    "time": dt,
                    "fields": dict_with_ints
                }]

                client.write_points(put_in_influx)

            except Exception as e:
                print(e)
                client.close()

            time.sleep(1)

a = ConnectTo()

def main():

    print("start")

    #try:

    a.readConfig(workpath="", confFileName="conf.cnfg", tagsFileName="opctags.cnfg")

    a.readData()

    #except Exception as e:
    #   print(e)

if __name__ == '__main__':
    main()
