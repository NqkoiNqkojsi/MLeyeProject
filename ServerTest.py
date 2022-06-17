#Import necessary libraries
from flask import Flask, render_template, Response, make_response
import video_streaming as vst
import cv2
#Initialize the Flask app
app = Flask(__name__)
camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''
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
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/result')
def result():
    response=make_response(str(vst.Stream()),200)
    response.mimetype="text/plain"
    return response
def result():
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0") 
