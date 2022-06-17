import numpy as np
import keras
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

model=keras.models.load_model('eye_state.h5')

def picture_anal(img):
  #make the dface and eyes detectors
  faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
  eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces=faceCascade.detectMultiScale(gray, 1.1, 4)
  if len(faces)<1:
    return 0
  for (x, y, w, h) in faces:
    gray = gray[y:y+int(h*0.6), x:x+w]
    img = img[y:y+int(h*0.6), x:x+w]
  #get the first 2 instances of eyes
  eyes = eyeCascade.detectMultiScale(gray, 1.3, 6)
  #draw the eye borders and show it
  img2=img.copy()
  if len(faces)<1:
    return 0
  for (x, y, w, h) in eyes:
    cv2.rectangle(img2, (x,y), (x+w, y+h), (0, 255, 0), 2)
  plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
  plt.show()
  eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  eyes = eyeCascade.detectMultiScale(gray, 1.1, 4)
  for x, y,w, h in eyes:
    print(x, y, w, h)
    roi_gray = gray[int(y*0.8):y+int(h*1.1), int(x*1):x+int(w*1.2)]
    roi_color = img[int(y*0.8):y+int(h*1.1), int(x*1):x+int(w*1.2)]
    eyess = eyeCascade.detectMultiScale(roi_gray)
    if len(eyess) == 0:
      print("eyes not detected")
    else:
      for ex, ey, ew, eh in eyess :
        eyes_roi = roi_color
        final_img = cv2.resize(eyes_roi, (64,64))
        final_img=cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
        final_img = np.expand_dims(final_img, axis=0)
        final_img = final_img/255.0
        if np.argmax(model.predict(final_img))==0:#0 is closed eyes, 1 is open
          return 0
  return 1

