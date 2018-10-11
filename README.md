# ml-workflow


Comments to cn-ad.cnfg.json file


{ 
  "object_name":{                                                               #название объекта: unit1/unit2...
    "channel_name":{                                                            #название канала - тег, например NGP, PCD...
      "input":{                                                                 #входные данные для модели
        "model_name":"ARIMA",                                                   #название используемое для типа модели
        "model_dir":"./object_name.channel_name.model_name.unix_time",          #директория где расположен файл модели 
        "rate":"1s"                                                             #частота запросов, здесь каждую секунду
        "fields":{                                                              #список полей для образа модели
          "channel.raw":""                                                      #тег параметра
        }
      },
      "output":{                                                                #выходные данные
        "node":"influxdb",                                                      #название службы для которой предназначены данные
        "database":"model_data",                                                #название базы данных
        "measurement":"object_name.channel_name.model_name.unix_time",          #название таблицы/measurement
          "fields":{                                                            #список полей для 
            "channel.live":"",                                                  #текущее значение
            "channel.redic":"",                                                 #предсказанное значение
            "channel.mse_error":""                                              #сре. квад. ошst_cnfgибка
            }
        }
     }
  }
}
