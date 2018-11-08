#! /usr/bin/python3
"""
Осноной скрипт веб-сервиса Flask
"""
import pickle
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from flask import Flask, request
from sklearn.metrics import mean_squared_error as mse
from statsmodels.tsa.holtwinters import ExponentialSmoothing

app = Flask(__name__)

@app.route('/ARIMA', methods = ['POST', 'GET'])

def apicall_two(responses2 = None):
    df = None
    path = None
    try:
        data_as_json = request.get_json()
        print(data_as_json)
        meta_data = data_as_json['meta_data']
        path = meta_data['model_path']
        df = pd.read_json(data_as_json['data_frame'], orient='columns')
        print(meta_data, df)
    except Exception as e:
        print(e)
    finally:
        print('pass step data_as_json = request.get_json()')
    results_of_model = statsmodels.tsa.statespace.sarimax.SARIMAXResults.load(path)
    
    my_mod_tag = sm.tsa.SARIMAX(df.astype(float), order=(1, 1, 1),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

    res_tag = my_mod_tag.filter(results_of_model.params)

    insample_tag = res_tag.predict(start=len(df.index), end=len(df.index))

    live = np.round(df[-1:].values, 5)

    my_list = map(lambda x: x[0], live)

    live_series = list(pd.Series(my_list))

    mse = live_series[0] - insample_tag.values[0]

    mse = pow(mse, 2)

    returning_data = list()

    returning_data.append(insample_tag.values.tolist()[0])
    returning_data.append(mse)
    returning_data.append(float(live))

    print(returning_data)

    return str(returning_data)


@app.route('/HOLTWINTER', methods = ['POST', 'GET'])

def apicall_t(responses2 = None):
    df = None
    path = None
    try:
        data_as_json = request.get_json()
        print(data_as_json)
        meta_data = data_as_json['meta_data']
        path = meta_data['model_path']
        df = pd.read_json(data_as_json['data_frame'], orient='columns')
        print(meta_data, df)

        #test_json = request.get_json()

        #gotten_data_as_df_with_model_dir = pd.read_json(test_json, orient='columns')

        #model_dir = str(gotten_data_as_df_with_model_dir.model_dir.unique()[0])

        #gotten_data_df = gotten_data_as_df_with_model_dir.drop(['model_dir'], axis=1)

    except Exception as e:
        print(e)

    print(path)

    with open('./models/holt_winter.pickle', 'rb') as handle:
        model1 = pickle.load(handle)
        live = np.round(df[-1:].values, 5)
        pred = model1.predict(start=len(df.index), end=len(df.index))  # param_data.index[-1])
        mse_ = mse(pred, df.iloc[-1:])

        returning_data = list()

        returning_data.append(pred.tolist()[0])
        returning_data.append(mse_)
        returning_data.append(float(live))
        print(returning_data)

    return str(returning_data)

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port=5003)