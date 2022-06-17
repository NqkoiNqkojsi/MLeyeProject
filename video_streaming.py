
# import the opencv library
import cv2
import FaceTest as fc
import time
import requests
#def Is_Active():
ip="http://192.168.1.8:5000"

def Stream():
    # define a video capture object
    vid = cv2.VideoCapture(0)
    while(True):
        ret, frame = vid.read()
        return fc.picture_anal(frame)


isActive=True
def StopVideo():
    isActive=False

def Main_Run(mode):
    isActive=True
    iter=0
    state=[1,1,1,1,1,1,1,1,1,1,1]
    while(isActive):
        for x in range(0, 10):
            state[x]=state[x+1]
        state[10]=Stream()
        if state.count(0)>7:
            if mode==0:
                r = requests.get(str(ip+"/taze"), auth=('user', 'pass'))
            else:
                r = requests.get(str(ip+"/vibrate"), auth=('user', 'pass'))
            time.sleep(0.5)