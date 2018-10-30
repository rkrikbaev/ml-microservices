#!/user/bin/python3
import json
from influxdb import InfluxDBClient, DataFrameClient

header = {'Content-Type': 'application/json', 'Accept': 'application/json'}

class Config(object):
	id = 0
	def loadInfo(self, **kwargs):
		file = kwargs['file']
		source_info = []
		model_info = []
		dest_info = []
		with open(file, 'r') as fp:
			list = json.load(fp)
			id = list.keys()
		for id in list:
			source_info.append(list[id]["source_fields"])
			model_info.append(list[id]["model_fields"])
			dest_info.append(list[id]["destination_fields"])
		return source_info, model_info, dest_info

class LinkData(object):
	def __init__(self, **kwargs):
		self.host = kwargs['host']
		self.port = kwargs['port']
		self.user = kwargs['user']
		self.password = kwargs['password']
		self.query = kwargs['query']
		self.db = kwargs['db']

	def _InfluxDfClient(self):
		client = DataFrameClient(self.host, self.port, self.db)
		data_as_df = client.query(self.query)
		data_as_df = dict(data_as_df)
		print(data_as_df)
		return data_as_df

	def getData(self, node=None):

		if node == 'influxdb':
			print('influxdb')
			data = self._InfluxDfClient()
		else:
			pass
		return print(data)

class Flow(object):
	def __init__(self):
		pass
	def execute(self):
		pass
		return(self)