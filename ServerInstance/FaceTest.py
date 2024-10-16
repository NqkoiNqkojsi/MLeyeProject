import numpy as np
import keras
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import os
class FaceTest:

  def __init__(self):
    self.model=keras.models.load_model('eye_state.h5')

  def load_images_from_folder(self, folder):
      images = []
      for filename in os.listdir(folder):
          img = cv2.imread(os.path.join(folder,filename))
          if img is not None:
              images.append(img)
      return images


  def picture_anal(self, img):
    #make the dface and eyes detectors
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    try:
      gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
      print("color problem")
      return 0
    faces=faceCascade.detectMultiScale(gray, 1.1, 4)
    print("number of faces = "+str(len(faces)))
    if len(faces)<1:
      print("no face detected")
      return 0
    for (x, y, w, h) in faces:
      gray = gray[y:y+int(h*0.6), x:x+w]
      img = img[y:y+int(h*0.6), x:x+w]
    #get the first 2 instances of eyes
    eyes = eyeCascade.detectMultiScale(gray, 1.3, 6)
    #draw the eye borders and show it
    img2=img.copy()
    print("number of eyes = "+str(len(eyes)))
    if len(eyes)<1:
      print("no eyes detected")
      return 0
    for (x, y, w, h) in eyes:
      cv2.rectangle(img2, (x,y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imwrite('test_video/frame1.jpg', img2)
    cv2.imshow('img2', img2)
    cv2.waitKey(1)
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eyeCascade.detectMultiScale(gray, 1.1, 4)
    for x, y,w, h in eyes:
      roi_gray = gray[int(y*0.8):y+int(h*1.1), int(x*1):x+int(w*1.2)]
      roi_color = img[int(y*0.8):y+int(h*1.1), int(x*1):x+int(w*1.2)]
      eyess = eyeCascade.detectMultiScale(roi_gray)
      if len(eyess) == 0:
        print("eyes not detected")
        return 0
      else:
        for ex, ey, ew, eh in eyess :
          eyes_roi = roi_color
          final_img = cv2.resize(eyes_roi, (64,64))
          final_img=cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
          final_img = np.expand_dims(final_img, axis=0)
          final_img = final_img/255.0
          if np.argmax(self.model.predict(final_img))==0:#0 is closed eyes, 1 is open
            print("found closed eye")
            return 0
    print("all eyes are open")
    return 1