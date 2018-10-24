import json, argparse

class Config(object):

    def __init__(self, **kwargs):
        self.file = kwargs

    def readModelsConfigFile(self, file=''):

        ID = 0

        with open(file, 'r') as fp:
            list = json.load(fp)
            id = list.keys()
            for id in list:
                item_id = id
                ml_core = list[id]["ml-core"]
                data_source = list[id]["source"]
                source_fields = list[id]["source_fields"]
                model_fields = list[id]["model_fields"]
                dest_fields = list[id]["destination_fields"]

                print(item_id, ml_core, data_source, source_fields, model_fields, dest_fields)


ConfigString = Config()

InfluxNodeConfig = ConfigString.readModelsConfigFile(file='./model.conf')
print(InfluxNodeConfig)

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
