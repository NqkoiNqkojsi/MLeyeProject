import numpy as np
import keras
import cv2
import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


#load the saved model
model=keras.models.load_model('eye_state.h5')
#get the img
img = cv2.imread('stelyo2.jpg')
plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
#make the dface and eyes detectors
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#get the first 2 instances of eyes
eyes = eyeCascade.detectMultiScale(gray, 1.1, 4)
#draw the eye borders and show it
img2=img.copy()
for (x, y, w, h) in eyes:
  cv2.rectangle(img2, (x,y), (x+w, y+h), (0, 255, 0), 3)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.show()
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
eyes = eyeCascade.detectMultiScale(gray, 1.1, 4)
for x, y,w, h in eyes:
  roi_gray = gray[y:y+h, x:x+w]
  roi_color = img[y:y+h, x:x+w]
  eyess = eyeCascade.detectMultiScale(roi_gray)
  if len(eyess) == 0:
    print("eyes not detected")
  else:
    for ex, ey, ew, eh in eyess :
      eyes_roi = roi_color[ey:ey+eh, ex:ex+ew]
      final_img = cv2.resize(eyes_roi, (64,64))
      final_img=cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
      final_img = np.expand_dims(final_img, axis=0)
      final_img = final_img/255.0
      label=np.argmax(model.predict(final_img))
      plt.imshow(cv2.cvtColor(eyes_roi, cv2.COLOR_BGR2RGB))
      plt.imshow(np.squeeze(final_img))
      plt.title(label)
      #print("Original label is {} and predicted label is {}".format(y_real, y_pred))
      print("predicted label is " +str(label))
      plt.show()
images=load_images_from_folder("random_img")
for x in images:
  final_img = cv2.resize(x, (64,64))
  final_img=cv2.cvtColor(final_img, cv2.COLOR_BGR2GRAY)
  final_img = np.expand_dims(final_img, axis=0)
  final_img = final_img/255.0
  label=np.argmax(model.predict(final_img))
  plt.imshow(np.squeeze(final_img))
  plt.title(label)
  #print("Original label is {} and predicted label is {}".format(y_real, y_pred))
  print("predicted label is " +str(label))
  plt.show()

