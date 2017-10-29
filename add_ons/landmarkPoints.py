import frontalize
import facial_feature_detector as feature_detection
import camera_calibration as calib
import scipy.io as io
import cv2
import numpy as np
import os
import check_resources as check
import matplotlib.pyplot as plt
import demo

cap = cv2.VideoCapture(0)
this_path = os.path.dirname(os.path.abspath(__file__))

while 1:
    ret, img = cap.read()
    demo()
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()