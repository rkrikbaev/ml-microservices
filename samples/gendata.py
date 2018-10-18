# -*- coding: utf-8 -*-
import urllib.request
import json
import time
import math
import _thread
import random
from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'commonRealTimeInfo')
client2 = InfluxDBClient('localhost', 8086, 'root', 'root', 'eventsRealTimeInfo')
client3 = InfluxDBClient('localhost', 8086, 'root', 'root', 'randomRealTimeInfo')

client.create_database('commonRealTimeInfo')
client2.create_database('eventsRealTimeInfo')
client3.create_database('randomRealTimeInfo')

genFuncs_angle = 0
genFuncs_line = 0
genRandBinaryFlag = 0
genTimeLineFlag = 1
genTimeLineState = 1

def generateFuncs(linemaxmin, rand, threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            # half-sinusoid and line for general testing
            global genFuncs_angle, genFuncs_line, genRandBinaryFlag, genTimeLineFlag, genTimeLineState
            genFuncs_angle += 1
            sin = math.sin(math.radians(genFuncs_angle))
            if genFuncs_angle >= 179: genFuncs_angle = 1

            if genFuncs_line < linemaxmin[0]: genFuncs_line = linemaxmin[0]
            genFuncs_line += 1
            if genFuncs_line > linemaxmin[1]: genFuncs_line = linemaxmin[0]

            json_body_lines = [
                {
                    "measurement": "lines",
                    "fields": {
                        "sinusoid": int(sin*100),
                        "sinangle": int(genFuncs_angle),
                        "stepline": int(genFuncs_line)
                    }
                }
            ]
            client3.write_points(json_body_lines)

            # general random generation, for usage in Timeline and others
            rand1 = random.randint(rand[0], rand[1])
            rand2 = random.randint(rand[0]*10, rand[1]*10)

            _randbin = random.randint(1, 300)
            randbin = 1
            if _randbin >= 299:
                genRandBinaryFlag = random.randint(20,40)

            # will generate series 20-40 of zeros, after triggering
            if genRandBinaryFlag > 0:
                randbin = 0
                genRandBinaryFlag -= 1


            if genTimeLineFlag > 0:
                genTimeLineFlag  -= 1
            else:
                genTimeLineState = random.randint(1, 4)
                genTimeLineFlag = random.randint(5, 50)

            json_body_random = [
                {
                    "measurement": "randomNumbers",
                    "fields": {
                        "rand": int(rand1),
                        "randX10": int(rand2),
                        "randbinary": int(randbin),
                        "timeline": int(genTimeLineState)
                    }
                }
            ]
            client3.write_points(json_body_random)

            # generate event text for PX-timeseries
            rand3 = random.randint(1,400)
            if rand3 >= 399: # eg 0.25 % prob
                eventString = "color:blue,icon:px-fea:asset,text:Обычное событие"
                rand4a = random.randint(1, 100)
                print ("%d rand4a" % rand4a)
                if rand4a >= 90:
                    eventString = "color:orange,icon:px-fea:deployments,text:Уникальное событие"
                    print ("we have UNIQ event %s" % eventString)
                elif rand4a >= 70:
                    eventString = "color:green,icon:px-fea:administration,text:Редкое событие"
                    print ("We have RARE event %s" % eventString)

                json_body_event = [
                    {
                        "measurement": "timeSeriesEvent",
                        "fields": {
                            "eventInfo": str("%s" % (eventString))
                        }
                    }
                ]
                client3.write_points(json_body_event)

        except Exception as e:
            print("%s Error generateFuncs: %s" % (threadName,str(e)))


def getExchange(currencycode,threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            url = 'https://free.currencyconverterapi.com/api/v6/convert?compact=ultra&q=%s' % currencycode
            req = urllib.request.Request(url)

            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))

            val = cont[currencycode]
            json_body = [
                {
                    "measurement": "exchange",
                    "tags": {
                        "base": "KZT",
                    },
                    "fields": {
                        "%s" % currencycode: float(val)
                    }
                }
            ]
            client.write_points(json_body)
        except Exception as e:
            print("%s Error getExchange: %s" % (threadName,str(e)))


def getCrypto(threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            url = 'https://api.coinmarketcap.com/v2/ticker/?limit=30'
            req = urllib.request.Request(url)

            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))['data']

            for item in cont.values():
                name = item['name']
                symbol = item['symbol']
                price = item['quotes']['USD']['price']
                volume24h = item['quotes']['USD']['volume_24h']
                marketcap = item['quotes']['USD']['market_cap']

                json_body = [
                    {
                        "measurement": "crypto",
                        "tags": {
                            "currency": "%s" % name
                        },
                        "fields": {
                            "symbol_string": str("%s" % (symbol)),
                            "price": float(price),
                            "volume24h": float(volume24h),
                            "marketcap": int(marketcap)
                        }
                    }
                ]

                client.write_points(json_body)


        except Exception as e:
            print("%s Error getCrypto: %s" % (threadName,str(e)))

def getWeather(threadName, delay):
    while 1:
        time.sleep(delay)
        try:
            url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202255777%20and%20u%3D\'C\'&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
            req = urllib.request.Request(url)

            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))

            wind = cont['query']['results']['channel']['wind']['speed']
            atmosphere = cont['query']['results']['channel']['atmosphere']['pressure']
            humidity = cont['query']['results']['channel']['atmosphere']['humidity']
            temp = cont['query']['results']['channel']['item']['condition']['temp']

            json_body = [
                {
                    "measurement": "weather",
                    "tags": {
                        "city": "Ala",
                    },
                    "fields": {
                        "wind":float(wind),
                        "atmosphere":float(atmosphere),
                        "humididty":float(humidity),
                        "temperature":float(temp)
                    }
                }
            ]
            client.write_points(json_body)
        except Exception as e:
            print("%s Error getWeather: %s" % (threadName,str(e)))


def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x

def getQuake(threadName, delay,distance):
    while 1:
        time.sleep(delay)
        try:
            url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=43.238949&longitude=76.889709&maxradiuskm=%s' % (distance)
            req = urllib.request.Request(url)

            r = urllib.request.urlopen(req).read()
            cont = json.loads(r.decode('utf-8'))
            counter = 0

            for item in cont['features']:
                timeKey = '%s-%s'% (item['properties']['time'],item['properties']['code'])
                queryString = 'SELECT "uniqkey" FROM "commonRealTimeInfo"."autogen"."quake" where "uniqkey" = \'%s\'' % (
                    timeKey)
                result = client.query(queryString)

                _wikiSearchCity = item['properties']['place']

                if len(result) == 0:
                    magnitude = item['properties']['mag']
                    title = item['properties']['title']
                    qtype = item['properties']['type']
                    status = item['properties']['status']
                    place = item['properties']['place']
                    code = item['properties']['code']
                    id = item['properties']['time']

                    severity = "information"
                    if float(magnitude) > 4.5:
                        severity = "warning"
                    if float(magnitude) > 4.5 and int(distance) == 1000:
                        severity = "error"
                    if int(distance) == 300:
                        severity = "important"

                    qtime = datetime.fromtimestamp(float(item['properties']['time']) / 1000).strftime("%Y-%m-%dT%H:%M:%SZ")
                    print("%s NEW EVENT km:%s --->%s [%s] %s" % (threadName, distance,timeKey,magnitude,qtime))

                    cityInfoText = "No info found"
                    try:
                        __wikiSearchCity = _wikiSearchCity.split("of ")[1]
                        wikiSearchCity = __wikiSearchCity.split(",")[0].strip()
                        wikiCityGetInfo = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&format=json&redirects&titles=%s' % (
                            wikiSearchCity)
                        req2 = urllib.request.Request(wikiCityGetInfo)
                        r2 = urllib.request.urlopen(req2).read()
                        cont2 = json.loads(r2.decode('utf-8'))
                        _cityInfoText = list(findkeys(cont2, 'extract'))[0]
                        cityInfoText = _cityInfoText.replace('\r', '').replace('\n', '')
                    except:
                        print("can't parse city Info...continue")


                    json_body = [
                        {
                            "measurement": "quake",
                            "tags": {
                                "maxRadiusAla": "%skm" % distance
                            },
                            "time": str(qtime),
                            "fields": {
                                "magnitude":float(magnitude),
                                "place_string":str("%s" % (place)),
                                "uniqkey": str("%s" % (timeKey))
                            }
                        }
                    ]
                    print(cityInfoText)
                    json_body2 = [
                        {
                            "measurement": "quakeEvents",
                            "time": str(qtime),
                            "fields": {
                                "id": str("%s" % (id)),
                                "title":  str("%s" % (title)),
                                "subtitle": str("%s" % (qtype)),
                                "severity": str("%s" % (severity)),
                                "date": str("%s" % (qtime)),

                                "messagetext": str("%s" % (cityInfoText)),

                                "alerttext": str("%s magnitude" % (status)),
                                "alertvalue": float(magnitude),

                                "assettext": str("%s" % (place)),
                                "assetvalue": str("%s" % (code)),

                                "uniqkey": str("%s" % (timeKey))
                            }
                        }
                    ]
                    print(severity)
                    client.write_points(json_body)
                    client2.write_points(json_body2)

        except Exception as e:
            print("%s Error getQuake: %s" % (threadName,str(e)))


def main():
    print("Started gathering statistics")
    try:
        _thread.start_new_thread(getQuake, ("Thread-Quake-1", 60, 300))
        _thread.start_new_thread(getQuake, ("Thread-Quake-2", 90, 1000))
        _thread.start_new_thread(getQuake, ("Thread-Quake-3", 120, 3000))
        _thread.start_new_thread(getWeather, ("Thread-Weather-4", 40))
        _thread.start_new_thread(getCrypto, ("Thread-Crypto-5", 55))
        _thread.start_new_thread(getExchange, ("USD_KZT","Thread-ExchRates-6", 150)) # max 100 requests per hour for exchange rates:
        _thread.start_new_thread(getExchange, ("EUR_KZT", "Thread-ExchRates-7", 153))
        _thread.start_new_thread(getExchange, ("RUB_KZT", "Thread-ExchRates-8", 156))
        _thread.start_new_thread(getExchange, ("CNY_KZT", "Thread-ExchRates-9", 159))
        _thread.start_new_thread(generateFuncs, ([10,140], [0,5] ,"Thread-Gen-10", 5)) # line [min,max] and rand [min,max]
    except Exception as e:
         print("Error: unable to start thread" + str(e))

    while 1:
        time.sleep(80)
        pass

if __name__ == "__main__":
    main()




#curl http://localhost:8086/query \
#  -d db=commonRealTimeInfo \
#  -d q='drop measurement "quake"'