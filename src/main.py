import cv2
import time
import datetime
import os 

cap = cv2.VideoCapture(0)

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

    for num in range(19):
        print(params[num], ':', cap.get(num))

def caputure(dirpath):
    ret, frame = cap.read()
    # resize the window
    # windowsize = (800, 600)
    # frame = cv2.resize(frame, windowsize)
    now = datetime.datetime.now()
    filename = f'{dirpath}/sfm_' + now.strftime('%Y%m%d_%H%M%S') + '.jpg'
    cv2.imwrite(filename, frame)
    # cv2.imshow(filename, frame)

if __name__ == "__main__":
    get_camera_propaties()
    dirpath = make_new_dir()
    count = 0
    while(True):
        count += 1
        caputure(dirpath)
        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count == 1:
            break

    cap.release()

