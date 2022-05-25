import numpy as np
import keras
import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import os

def plot_imgs(directory, top=10):
    all_item_dirs = os.listdir(directory)
    item_files = [os.path.join(directory, file) for file in all_item_dirs][:5]
  
    plt.figure(figsize=(20, 20))
  
    for i, img_path in enumerate(item_files):
        plt.subplot(10, 10, i+1)
    
        img = plt.imread(img_path)
        plt.tight_layout()         
        plt.imshow(img, cmap='gray') 

def DisplayRes(image_number, x_test, y_test, model):
    labels = '''airplane automobile bird cat deer dog frog horse ship truck'''.split(sep=' ') 
    # display the image
    plt.imshow(x_test[image_number])
    # load the image in an array
    n = np.array(x_test[image_number])
    # reshape it
    p = n.reshape(1, 32, 32, 3)
    # pass in the network for prediction and
    # save the predicted label
    predicted_label = labels[model.predict(p).argmax()]
    # load the original label
    original_label = labels[int(y_test.flat[image_number])]
    # display the result
    plt.title("{} : {}".format(original_label, predicted_label))
    print("Original label is {} and predicted label is {}".format(original_label, predicted_label))
    plt.show()

data_path = 'dataset/train'

directories = ['/Closed_Eyes', '/Open_Eyes']
'''
for j in directories:
    plot_imgs(data_path+j)
'''
batch_size = 32
train_datagen = ImageDataGenerator(horizontal_flip = True, 
                                  rescale = 1./255, 
                                  zoom_range = 0.2, 
                                  validation_split = 0.1)

test_datagen = ImageDataGenerator(rescale = 1./255)
train_data_path = 'dataset/train'
test_data_path = 'dataset/test'

train_set = train_datagen.flow_from_directory(train_data_path, target_size = (64,64),
                                              batch_size = batch_size, 
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_data_path, target_size = (64,64),
                                              batch_size = batch_size, 
                                              color_mode = 'grayscale',
                                              class_mode = 'categorical')

classes = 2

model = Sequential()
model.add(Conv2D(32, (3,3), padding = 'same', input_shape = (64,64,1), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(64, (3,3), padding = 'same', activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(128,(3,3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2))) 

model.add(Flatten())

model.add(Dense(64, activation = 'relu'))

model.add(Dense(classes, activation = 'softmax'))

print(model.summary())
model.compile(loss = 'categorical_crossentropy',optimizer = 'adam' , metrics = ['accuracy'])
model_path="yawn_detection.h5"

checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', verbose=1, 
                              save_best_only=True, mode='max')

callbacks_list = [checkpoint]
num_epochs = 20
training_steps=train_set.n//train_set.batch_size
validation_steps =test_set.n//test_set.batch_size
history = model.fit_generator(train_set, epochs=num_epochs, steps_per_epoch=training_steps,validation_data=test_set,
                    validation_steps=validation_steps, callbacks = callbacks_list)
for x in range(0, 20):
    x, y_real = next(test_set)
    y_pred=np.argmax(model.predict(x))
    image = x[0]
    plt.imshow(np.squeeze(image))
    # display the result
    #plt.title("{} : {}".format(y_real, y_pred))
    plt.title(y_pred)
    #print("Original label is {} and predicted label is {}".format(y_real, y_pred))
    print("predicted label is " +str(y_pred))
    plt.show()