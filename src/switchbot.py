import os
import time
import hashlib
import hmac
import base64
import requests
import json
import uuid


def make_request_header() -> dict:
    # Declare empty header dictionary
    apiHeader = {}
    # open token
    token = 'e67ee428b00422c5189309e7907a2b16d8a5f1f95c703cdf9925ab6d696c2362a03ea97097173314c33c28b934950bc6' # copy and paste from the SwitchBot app V6.14 or later
    # secret key
    secret = '4546afba9093d230e5539b60eb88af34' # copy and paste from the SwitchBot app V6.14 or later
    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    print ('Authorization:{}'.format(token))
    print ('t:{}'.format(t))
    print ('sign:{}'.format(str(sign, 'utf-8')))
    print ('nonce:{}'.format(nonce))

    #Build api header JSON
    apiHeader['Authorization']=token
    apiHeader['Content-Type']='application/json'
    apiHeader['charset']='utf8'
    apiHeader['t']=str(t)
    apiHeader['sign']=str(sign, 'utf-8')
    apiHeader['nonce']=str(nonce)
    # print(apiHeader)
    # Header = json.dumps(apiHeader)
    return apiHeader


base_url = 'https://api.switch-bot.com'

def get_device_list(deviceListJson='deviceList.json'):
    # tokenとsecretを貼り付ける


    devices_url = base_url + "/v1.1/devices"

    headers = make_request_header()
    print(devices_url)
    print(headers)

    try:
        # APIでデバイスの取得を試みる
        res = requests.get(devices_url, headers=headers)
        print(devices_url)
        # res.raise_for_status()

        print(res.text)
        deviceList = json.loads(res.text)
        # 取得データをjsonファイルに書き込み
        with open(deviceListJson, mode='wt', encoding='utf-8') as f:
            json.dump(deviceList, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print('response error:',e)




if __name__ == "__main__":
    get_device_list()