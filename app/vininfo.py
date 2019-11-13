import json
import requests

'''
No real error checking is done on their end be careful
'''


def getInfo(info, toget):
    if info == None or toget not in info.keys():
        print("No " + toget.lower() + " info found")
        return ''
    else:
        return info[toget]


def getInfoFromVIN(vin, toget):
    return getInfo(getVehicleInfo(vin), toget)


def getYear(inf):
    return getInfo(inf, 'ModelYear')


def getModel(inf):
    return getInfo(inf, 'Model')


def getMake(inf):
    return getInfo(inf, 'Make')


def getVehicleInfo(vin):
    if not vin.isalnum():
        print("Invalid VIN")
        return None
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    post_fields = {'format': 'json', 'data': vin}
    r = requests.post(url, data=post_fields)
    response = json.loads(r.text)['Results'][0]
    results = dict()

    for k, v in json.loads(r.text)['Results'][0].items():
        if v != '':
            results[k] = v

    return results
