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
    token = "f7958620709d165f52d7509e8c34de0b780ce4b6f513c938c12946ddd8cfd4393e3287d56c290ce9c3db06a2d551991f" # copy and paste from the SwitchBot app V6.14 or later
    # secret key
    secret = "86a21e95224a02fa4b0962d674f90a8a" # copy and paste from the SwitchBot app V6.14 or later
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