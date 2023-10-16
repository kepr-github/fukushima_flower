import cv2
import time
import datetime
import os
import serial
import time
import schedule
import numpy as np
import winsound
import logging

# getLoggerにモジュール名を与える(このファイルを直接実行する場合は__main__になります)
logger = logging.getLogger(__name__)
# これを設定しておかないと後のsetLevelでDEBUG以下を指定しても効かないっぽい
logger.setLevel(logging.DEBUG)

# 出力先を指定している(今回はtest.logというファイルを指定)
handler = logging.FileHandler('./logs/test.log')

# そのハンドラの対象のレベルを設定する(今回はDEBUG以上)
handler.setLevel(logging.DEBUG)

# どんなフォーマットにするかを指定する。公式に使える変数は書いてますね。
formatter = logging.Formatter('%(levelname)s  %(asctime)s  [%(name)s] %(message)s')
handler.setFormatter(formatter)

# 設定したハンドラをloggerに適用している
logger.addHandler(handler)


#set up your serial port with the desire COM port and baudrate.
signal = serial.Serial('COM3', baudrate=9600, bytesize=8, stopbits=1, timeout=.1)
cap = cv2.VideoCapture(0)

def makesound():
    frequency = 1000
    duration = 100
    winsound.Beep(frequency, duration)

def turnon(secound):
    signal.write("AT+CH1=1".encode())
    time.sleep(8)
    signal.write("AT+CH1=0".encode())


def make_new_dir():
    now = datetime.datetime.now()
    dirname = './output/' + now.strftime('%Y%m%d%H%M')
    os.mkdir(dirname)
    return dirname

def get_camera_propaties():
    params = ['MSEC',
            'POS_FRAMES',
            'POS_AVI_RATIO',
            'FRAME_WIDTH',
            'FRAME_HEIGHT',
            'PROP_FPS',
            'PROP_FOURCC',
            'FRAME_COUNT',
            'FORMAT',
            'MODE',
            'BRIGHTNESS',
            'CONTRAST',
            'SATURATION',
            'HUE',
            'GAIN',
            'EXPOSURE',
            'CONVERT_RGB',
            'WHITE_BALANCE',
            'RECTIFICATION']

#    for num in range(19):
#        print(params[num], ':', cap.get(num))

def caputure(dirpath):
    ret, frame = cap.read()
    # resize the window
    # windowsize = (800, 600)
    # frame = cv2.resize(frame, windowsize)
    now = datetime.datetime.now()
    filename = f'{dirpath}/sfm_' + now.strftime('%Y%m%d_%H%M%S') + '.jpg'
    cv2.imwrite(filename, frame)
    # cv2.imshow(filename, frame)

def main():
    # turnon(10)
    logger.debug(datetime.datetime.now().strftime('%Y%m%H%M%S'))
    makesound()
    signal.write("AT+CH1=1".encode())
    get_camera_propaties()
    dirpath = make_new_dir()
    # count = 0
    basetime  = time.time()
    while(True):
        # count += 1
        caputure(dirpath)
        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if time.time()-basetime > 30:
            break

    cap.release()
    signal.write("AT+CH1=0".encode())
    logger.debug('finish')


if __name__ == "__main__":
    main()
    schedule.every(5).minutes.do(main)
    while True:
        logger.debug("running")
        schedule.run_pending()
        time.sleep(1)

