#Import necessary libraries
import asyncio
from flask import Flask, render_template, Response, make_response, request, url_for, flash, redirect
import aiohttp
import video_streaming as vst
import cv2
#Initialize the Flask app
app = Flask(__name__, template_folder='template')
camera = cv2.VideoCapture(0)
async def StartVideo(mode, ip):
    task = asyncio.create_task(vst.Main_Run(mode, ip))
    await task
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames())
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
def idx():
    message = ''
    if request.method == 'POST':
        user_IP = request.form.get('user_IP')
        vst.SetIp(user_IP)
        set_action = request.form.get('settings')
        asyncio.run(StartVideo(set_action, user_IP))
        print(str(user_IP)+"; "+str(set_action))
    return render_template('index.html', message=message)


if __name__ == "__main__":
    app.run(debug=True) 
