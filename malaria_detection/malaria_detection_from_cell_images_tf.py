# -*- coding: utf-8 -*-
"""Malaria_Detection_from_Cell_Images_tf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-pqP7KIPl_qwdz5XXeYOZwWDTVaEM9MS

# Malaria Detection from Cell Images

Dataset link: https://www.kaggle.com/datasets/iarunava/cell-images-for-detecting-malaria

Same or similar datasets can be obtained from the official [NIH Website](https://ceb.nlm.nih.gov/repositories/malaria-datasets/)

The dataset contains 2 folders

1. Infected
2. Uninfected

And a total of `27,558` images.
"""

#  install opendatasets and splitfolders, if not installed already
!pip install opendatasets
!pip install split-folders

# Commented out IPython magic to ensure Python compatibility.
# import required libraries
import numpy as np
import pandas as pd
import opendatasets as od
import splitfolders
import itertools
import base64
import io, os, signal
import shutil
from shutil import copy
from shutil import copytree, rmtree
import matplotlib.pyplot as plt
# % matplotlib inline
from PIL import Image
import cv2
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from google.colab import files
from tensorflow.keras.preprocessing import image

# Check Tensorflow and Keras version; check if GPU is available
print('Tensorflow version:', tf.__version__)
print('Keras version:', tf.keras.__version__)
print("GPU is", "available" if tf.config.list_physical_devices('GPU') else "NOT AVAILABLE")

# set seed
tf.random.set_seed(1)

# download the dataset
od.download("https://www.kaggle.com/datasets/iarunava/cell-images-for-detecting-malaria")

# create dataset folder and set folder variables
dir = 'dataset'
parent_dir = './cell-images-for-detecting-malaria'
path = os.path.join(parent_dir, dir)
os.mkdir(path)

base_dir = './cell-images-for-detecting-malaria/cell_images/cell_images/'
dataset_dir = './cell-images-for-detecting-malaria/dataset/'

# split data into train, val and test
input_folder = base_dir
output = dataset_dir
splitfolders.ratio(input_folder, output=output, 
                   seed=42, ratio=(.7, .2, .1), 
                   group_prefix=None)

# Check the dataset folder
!ls ./cell-images-for-detecting-malaria/dataset/

# cleanup
if os.path.exists('./cell-images-for-detecting-malaria/cell_images'):
    shutil.rmtree('./cell-images-for-detecting-malaria/cell_images')

"""## EDA"""

# Number of images in each class in 'train', 'val' and 'test

train_dir = os.path.join(dataset_dir, 'train')
val_dir = os.path.join(dataset_dir, 'val')
test_dir = os.path.join(dataset_dir, 'test')
class_names = os.listdir(train_dir)

print('Number of cell image classes in train:', len(os.listdir(train_dir)))
print(os.listdir(train_dir))
for cls in os.listdir(train_dir):
    print(cls, ':', len(os.listdir(train_dir + '/' + cls)))


print('\nNumber of cell image classes in val:', len(os.listdir(val_dir)))
print(os.listdir(val_dir))
for cls in os.listdir(val_dir):
    print(cls, ':', len(os.listdir(val_dir + '/' + cls)))


print('\nNumber of cell image classes in test:', len(os.listdir(test_dir)))
print(os.listdir(test_dir))
for cls in os.listdir(test_dir):
    print(cls, ':', len(os.listdir(test_dir + '/' + cls)))

print('\nClass names:', class_names)

# let's see what the filenames look like
print(os.listdir(train_dir + '/' + 'Parasitized')[:5])
print(os.listdir(train_dir + '/' + 'Uninfected')[:5])

# Visualize one image from each class - 'Parasitized' and 'Uninfected'
ppic = './cell-images-for-detecting-malaria/dataset/train/Parasitized/C57P18thinF_IMG_20150729_111518_cell_253.png'
upic = './cell-images-for-detecting-malaria/dataset/train/Uninfected/C138P99ThinF_IMG_20151005_173241_cell_54.png'

plt.figure(1, figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.imshow(cv2.imread(ppic))
plt.title("Parasitized cell")
plt.xticks([]) , plt.yticks([])

plt.subplot(1, 2, 2)
plt.imshow(cv2.imread(upic))
plt.title('Uninfected cell')
plt.xticks([]) , plt.yticks([])

plt.show()

"""## Data preprocessing"""

# Parameters for the loader
batch_size = 32
img_height = 128
img_width = 128
seed = 123
class_mode = 'binary'
color_mode = 'rgb'

# All images will be rescaled by 1./255 + image augmentation
train_datagen = ImageDataGenerator(
      rescale=1.0/255,
      rotation_range=20,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest'
    )

val_datagen = ImageDataGenerator(rescale=1.0/255)
test_datagen = ImageDataGenerator(rescale=1.0/255)

# Flow training images in batches using train_datagen generator
train_ds = train_datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(img_height, img_width),  # All images will be resized
        batch_size=batch_size,
        shuffle=True,
        class_mode=class_mode,
        color_mode=color_mode
    )

# Flow val images in batches using val_datagen generator
val_ds = val_datagen.flow_from_directory(
        val_dir,  # This is the source directory for training images
        target_size=(img_height, img_width),  # All images will be resized
        batch_size=batch_size,
        shuffle=True,
        class_mode=class_mode,
        color_mode=color_mode
    )

# Flow test images in batches using test_datagen generator
test_ds = test_datagen.flow_from_directory(
        test_dir,  # This is the source directory for training images
        target_size=(img_height, img_width),  # All images will be resized
        batch_size=batch_size,
        shuffle=False,
        class_mode=class_mode,
        color_mode=color_mode
    )

# Let's look at 1 of the the batches
train_batch = train_ds[0]
images, labels = list(train_batch)
print(images.shape)
print(labels.shape)

first_image = images[0]
first_image

# val_batch = val_ds[0]
# print(val_batch[0].shape)
# print(val_batch[1])
# test_batch = test_ds[0]
# print(test_batch[0].shape)
# print(test_batch[1])

first_image[:3, :3, 0]

"""## Build model"""

# CNN model with dropout layer
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', 
                           input_shape=(img_height, img_width, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(loss='binary_crossentropy',
              optimizer=Adam(learning_rate=1e-4),
              metrics=['accuracy'])

model.summary()

"""## Training"""

# callbacks
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    verbose=2
)

# Fit the model
history = model.fit(
      train_ds,
      steps_per_epoch=600,  # Total train images = batch_size * steps
      epochs=30,
      validation_data=val_ds,
      validation_steps=170,  # Total val images = batch_size * steps
      callbacks=[early_stopping],
      verbose=2)

# plot loss and accuracy

plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.grid()
plt.legend(fontsize=15)

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.grid()
plt.legend(fontsize=15)

# evaluate on test data
model.evaluate(test_ds, verbose=2)

# save the model
model.save('./cell-images-for-detecting-malaria/malaria_detection_cnn_tf.h5')

# make some predictions
predictions = model.predict(test_ds)
predictions = tf.nn.softmax(predictions)
labels = np.argmax(predictions, axis=1)

print(test_ds[60][1])
print(labels[:4])

"""### Test predictions on cell images from internet"""

# Upload malaria images here and have it classified

uploaded = files.upload()

for fn in uploaded.keys():
 
  # predicting images
  path = '/content/' + fn
  img = image.load_img(path, target_size=(128, 128))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  print(classes[0])
  if classes[0]>0.5:
    print(fn + " is Unintefcted")
  else:
    print(fn + " is Parasitized")

"""## Next steps:
1. Add visualizations for predictions
2. Use transfer learning and compare results
"""