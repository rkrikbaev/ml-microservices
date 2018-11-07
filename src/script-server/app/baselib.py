#!/user/bin/python3
"""

Основная библиотека по которой строится workflow

"""
import argparse
import json, requests
import pandas as pd
from influxdb import DataFrameClient

class Config(object):
    def __init__(self, **kwargs):
        pass

    def _loadJson(self,file):
        with open(file, 'r') as fp:
            list = json.load(fp)
        return list

    def getInfo(self, **kwargs):
        file = kwargs['file']
        list ={}
        config_list = self._loadJson(file)
        for item in config_list:
            print(config_list[item]['enabled'])
            if config_list[item]['enabled'] == True:
                list[item] = config_list[item]
        return list


class Link(object):
    def __init__(self, host, port, user, password, id_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.id_name = id_name
        self.data = None
        self.query = None

    def getData(self, query, node, database, **kwargs):     #через influxdb.DataFrameClient методом query() возвращаяет данные в формате датафрейм (dataframe)
        self.query = query
        data_as_list_df = None
        try:
            if node == 'influxdb':
                data_as_list_df = self.influxdb_client(method='get', database = database)
        except Exception as e:
            print(e)
        finally:
            return (data_as_list_df)

    def putData(self, data, node, database, **kwargs):      #через influxdb.DataFrameClient write_points() записывает данные в формате JSON
        try:
            if node == 'influxdb':
                self.influxdb_client(data=data, method='put', database=database)
        except Exception as e:
            print(e)
        finally:
            #print('passing Link.putData with id {0}'.format(self.id_name))
            pass

    def influxdb_client(self, **kwargs):
        method = kwargs['method']
        database = kwargs['database']
        data_as_list_df = None
        try:
            if method == 'get':
                client_get = DataFrameClient(self.host, self.port, database)
                data_as_list_df = client_get.query(self.query)
            if method == 'put':
                data_as_df = kwargs['data']
                client_put = DataFrameClient(self.host, self.port, database=database)
                client_put.write_points(data_as_df, measurement=self.id_name, protocol='json')
        except Exception as e:
            print(e)
        finally:
            #print('passing Link.influxdb_client() with id {0}'.format(self.id_name))
            return data_as_list_df
class Model(object):
    def __init__(self, host, port, node, core, id_name, **kwargs):
        self.host = host
        self.port = port
        self.node = node
        self.core = core
        self.id_name = id_name
        self.path = None
        self.type = None
        self.data = None
        self.tag = None
        self.df_time = None
    def execModel(self, path, type, data, tag, **kwargs):
        self.path = path
        self.type = type
        self.data = data
        self.tag = tag
        calc_data_as_df = None

        try:
            if self.core == 'tf-core':
                data_as_json = self.prep_data(self.data, self.tag, operation='to_json')
                calc_data = self._tf_core(data_as_json)
                calc_data_as_df = self.prep_data(calc_data, self.tag, operation='to_df')
            else: pass
            if self.core == 'flask-core':
                data_as_json = self.prep_data(self.data, self.tag, operation='to_json')
                calc_data = self._flask_core(data_as_json)
                calc_data_as_df = self.prep_data(calc_data, self.tag, operation='to_df')
            else: pass
        except Exception as e:
            print(e)
        finally:
            #print('passing model.execModel, id {0}'.format(self.id_name), 'on ml-core {0}'.format(self.core))
            return calc_data_as_df

    def _tf_core(self, data_as_json):
        returning_data = None
        try:
            mse = 1
            #print(data_as_json)
            df = data_as_json['data_frame']
            df = df.split(']')
            df = df[0].split('[')
            df = df[1]
            df_as_json = json.dumps({"inputs":float(df)})
            json_response = requests.post("http://{0}:{1}/{2}".format(self.host, self.port, self.path), data=df_as_json)
            response = json.loads(json_response.text)
            print(response)
            predicted_value = response['outputs']
            returning_data = list()
            returning_data.append(predicted_value)
            returning_data.append(mse)
            returning_data.append(float(df))
        except Exception as e:
            print(e)
        finally:
            #print('passing model.execModel._tf_core, id {0}'.format(self.id_name))
            return returning_data

    def _flask_core(self, data_as_json):
        response = None
        header = {'Content-Type': 'application/json', 'Accept': 'application/json' }
        try:
            response = requests.post(
                url='http://{0}:{1}/{2}'.format(self.host, self.port, self.type),
                data=json.dumps(data_as_json), headers=header)
        except Exception as e:
            print(e)
        finally:
            #print('passing model.execModel._flask_core, id {0}'.format(self.id_name))
            return response.json()

    def prep_data(self, data, tag, operation=''):

        meta_data = {"model_type":self.type,
                     "model_path":self.path,
                     "id_name":self.id_name}
        try:
            if operation=='to_json':
                df = pd.concat(data)
                self.df_time = df
                df = df.reset_index()
                df = df[self.tag]
                data_array = df.values
                df_as_json = pd.Series(data_array).to_json(orient='records')
                data_as_json = {"data_frame": df_as_json,
                                "meta_data": meta_data}
                return data_as_json
            if operation == 'to_df':
                df = self.df_time.reset_index()
                df = df.set_index('level_1')
                data_as_df = pd.DataFrame([data], columns=[tag+".predicted", tag+".mse", tag+".actual"], index=df[-1:].index)
                return data_as_df
        except Exception as e:
            print(e)
        finally:
            #print('passing model.execModel.prep_data, id {0}'.format(self.id_name))
            pass