import numpy as np
import cv2
import dlib
import webbrowser
import scipy

PREDICTOR_PATH = "C:\Users\ASUS\PycharmProjects\cvdrive\dlib_models\shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eye_num = 0
        counter = 0
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye_num += 1
            cv2.rectangle(roi_color, (ex,ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        if eye_num == 0:
            counter += 2
        if eye_num == 1:
            counter += 1

        if eye_num >= 2:
            counter = 0
        #if counter > 9:
         #   webbrowser.open("/home/yishayrl/IdeaProjects/a.mp3")

    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()