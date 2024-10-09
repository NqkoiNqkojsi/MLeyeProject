# import the opencv library
import asyncio
import cv2
import FaceTest as face
import time
import requests
import base64
import PIL.Image
import os
import io

 
ip="192.168.1.10:5000"
faceClassifier=face.FaceTest()
def Stream():
    # define a video capture object
    vid = cv2.VideoCapture("test_img/todor.jpg")
    ret, frame = vid.read()
    base64_bytes = base64.b64encode(frame)
    print(type(base64_bytes))
    ENCODING = 'utf-8'
    # third: decode these bytes to text
    # result: string (in utf-8)
    base64_string = base64_bytes.decode(ENCODING)
    return faceClassifier.picture_anal(frame)
 
 
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
    state=[1,1,1,1,1,1]
    while(True):
        for x in range(0, 5):
            state[x]=state[x+1]
        state[5]=Stream()
        print(state)
        if isAsleep==True and state[5]==1:
            state=[0,0,1,1,1,1]
            isAsleep=False
        if state.count(0)>2:
            isAsleep=True
            try:
                if mode==0:
                    r = requests.get(str("http://"+ip+"/taze"), auth=('user', 'pass'))
                else:
                    r = requests.get(str("http://"+ip+"/vibrate"), auth=('user', 'pass'))
            except:
                pass
        time.sleep(1)
 
def Test_run(mode):
    isActive=True
    iter=0
    state=[1,1,1,1,1,1,1,1,1,1,1]
    while(isActive):
        for x in range(0, 10):
            state[x]=state[x+1]
        state[10]=faceClassifier.picture_anal(cv2.imread('test_img/stelyo2.jpg'))
        if state.count(0)>7:
            if mode==0:
                r = requests.get(str("http://"+ip+"/taze"), auth=('user', 'pass'))
            else:
                r = requests.get(str("http://"+ip+"/vibrate"), auth=('user', 'pass'))
        time.sleep(0.5)

class PackageState:
    def __init__(self, state, isAsleep, ip, mode):
        self.state = state
        self.isAsleep = isAsleep
        self.ip=ip
        self.mode=mode
    img=cv2.imread('test_img/empty.jpg')
    

    def MakeImageJson(self):
        file='test_video/frame1.jpg'
        to_send=PIL.Image.open(file)
        with io.BytesIO() as buf:
            to_send.save(buf, 'jpeg')
            image_bytes = buf.getvalue()
            base64_bytes = base64.b64encode(image_bytes)
            ENCODING = 'utf-8'
            # third: decode these bytes to text
            # result: string (in utf-8)
            base64_string = base64_bytes.decode(ENCODING)
            return base64_string

    def ReturnDic(self):
        return {
        "state": self.state,
        "isAsleep": self.isAsleep,
        "ip": self.ip,
        "mode":self.mode,
        "img":self.MakeImageJson()
        }
    
    


def Site_Oriented(pack):
    print("ip="+pack.ip)
    for x in range(0, 5):
        pack.state[x]=pack.state[x+1]
    pack.state[5]=faceClassifier.picture_anal(pack.img)
    print(pack.state)
    if pack.isAsleep==True and pack.state[5]==1:
        pack.state=[0,0,1,1,1,1]
        pack.isAsleep=False
        return pack.state
    if pack.state.count(0)>2:
        pack.isAsleep=True
        try:
            if pack.mode==0:
                r = requests.get(str("http://"+pack.ip+"/taze"), auth=('user', 'pass'))
            else:
                r = requests.get(str("http://"+pack.ip+"/vibrate"), auth=('user', 'pass'))    
        except:
            pass
    return pack 
        
if __name__ == "__main__":
    Main_Run(1,ip)
