# Reference from: https://github.com/SHAIK-AFSANA/facialemotionrecognizerinrealtime
# Title: Mirror, Mirror

from tensorflow import keras
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import serial
import time

face_classifier = cv2.CascadeClassifier(r'MirrorMirror/haarcascade_frontalface_default.xml')
classifier =load_model(r'MirrorMirror/model.h5')

# 7 different emotions are defined, but for this project, only 5 of them are used
emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']

# Setup serial connection (Make sure to use the correct COM port)
ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

cap = cv2.VideoCapture(0)



while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

            # Prediction and emotion detection
            if label == 'Angry':
                ser.write(b'R')
            elif label == 'Fear':
                ser.write(b'P')
            elif label == 'Happy':
                ser.write(b'G')
            elif label == 'Sad':
                ser.write(b'B')
            elif label == 'Neutral':
                ser.write(b'Y')
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            ser.write(b'Y')  # Default to yellow if no face  detected

    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()  # Close the serial connection