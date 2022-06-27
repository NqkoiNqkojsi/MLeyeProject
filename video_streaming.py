# import the opencv library
import asyncio
import cv2
import FaceTest as fc
import time
import requests
 
ip="192.168.1.10:5000"
 
def Stream():
    # define a video capture object
    vid = cv2.VideoCapture(0)
    ret, frame = vid.read()
    return fc.picture_anal(frame)
 
 
def Setup():
    global isActive
    isActive=False
 
 
 
def SetIp(ipAddr):
    ip=ipAddr
 
def Main_Run(mode, ip):
    print("ip="+ip)
    isAsleep=False
    isActive=True
    iter=0
    state=[1,1,1,1,1,1,1,1]
    while(True):
        for x in range(0, 7):
            state[x]=state[x+1]
        state[7]=Stream()
        print(state)
        if isAsleep==True and state[7]==1:
            state=[0,0,0,1,1,1,1,1]
            isAsleep=False
        if state.count(0)>4:
            isAsleep=True
            try:
                if mode==0:
                    r = requests.get(str("http://"+ip+"/taze"), auth=('user', 'pass'))
                else:
                    r = requests.get(str("http://"+ip+"/vibrate"), auth=('user', 'pass'))
                time.sleep(1)
            except:
                
                return
 
def Test_run(mode):
    isActive=True
    iter=0
    state=[1,1,1,1,1,1,1,1,1,1,1]
    while(isActive):
        for x in range(0, 10):
            state[x]=state[x+1]
        state[10]=fc.picture_anal(cv2.imread('test_img/stelyo2.jpg'))
        if state.count(0)>7:
            if mode==0:
                r = requests.get(str("http://"+ip+"/taze"), auth=('user', 'pass'))
            else:
                r = requests.get(str("http://"+ip+"/vibrate"), auth=('user', 'pass'))
        time.sleep(0.5)

if __name__ == "__main__":
    Main_Run(1,ip)
