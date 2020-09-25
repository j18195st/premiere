# -*- coding:utf-8 -*-

import json
import urllib.parse
import urllib.request
import time


def get_api():
    with open('static.json', 'r') as f:
        data = json.load(f)
        print(data)
        return data


def get_vt_data(key, hash):
    import requests
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': key, 'resource': hash}
    di = requests.get(url, params=params)

    print(di['permalink'])
    print('Score >> ' + str(di['positives']) + "/" + str(di['total']))
    time.sleep(30)
    # print(response.json())


if __name__ == '__main__':
    data = get_api()
    api, hash = data['api'], data['hash']
    get_vt_data(api, hash)
