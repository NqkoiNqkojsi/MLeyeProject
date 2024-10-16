#Import necessary libraries
import asyncio
from flask import Flask, render_template, Response, make_response, request, url_for, flash, redirect, jsonify
import aiohttp
import video_streaming as vst
import cv2
import base64

#Initialize the Flask app
app = Flask(__name__, template_folder='template')
camera = cv2.VideoCapture(0)


def gen_frames(pack):
      
    success, frame = camera.read()  # read the camera frame
    if not success:
        img=cv2.imread('test_img/empty.jpg')
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
    else:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def ReturnInfo(pack): 
    vid = cv2.VideoCapture(0)
    ret, frame = vid.read()  # read the camera frame
    pack.img=frame
    return vst.streamToSite(pack)
        

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/start_feed', methods=['POST'])
def start_feed():
    data=request.json
    pack=vst.PackageState(data["state"], data["isAsleep"], data["ip"], data["mode"])
    return jsonify(ReturnInfo(pack).ReturnDic())
'''
@app.route('/result')
def result():
    response=make_response(str(vst.Stream()),200)
    response.mimetype="text/plain"
    return response
'''
@app.route('/video', methods=['post', 'get'])
def video():
    message = ''
    if request.method == 'POST':
        pass
    return render_template('index.html', message=message)


@app.route('/index', methods=['post', 'get'])
async def idx():
    message = ''
    if request.method == 'POST':
        user_IP = request.form.get('user_IP')
        vst.SetIp(user_IP)
        set_action = request.form.get('settings')
        await vst.Main_Run(set_action, user_IP)
        print(str(user_IP)+"; "+str(set_action))
    return render_template('index.html', message=message)


if __name__ == "__main__":
    app.run(debug=True) 
