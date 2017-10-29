#Project done by Lior Kleinman, Yishy Harel and Yael Berger

import numpy
import cv2
import dlib
import webbrowser
import scipy
import math
import time
import sys
import winsound

#initialize default values
number_of_seconds = 1
show = True
music =  'Yishy.wav'

#get modified values from the user via the GUI:
if ((len(sys.argv) != 1)):
    #1. check if the user would like to see the video
    if (sys.argv[1] == "view"):
        show = True
    else:
        show = False

    #2. alert states the way the user would like to be alerted
    alert = sys.argv[2]
    if (alert == "rock"):
        music = 'rock.wav'
    elif (alert == "mozart"):
        music = 'mozart.wav'
    else:
        music = 'yishy.wav'
    #3. apply the user's pick as the time treshold (in seconds)
    number_of_seconds = int(sys.argv[3])

# Notify the user to press the 'esc' button in order to close the window.
if (show == True):
    print ("\n\nPress the 'esc' button to exit\n")

#define the predicator path for the '68 face landmark points' and Haar-Cascade methods and xml files:
PREDICTOR_PATH = r"dlib_models\shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(PREDICTOR_PATH)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# get liveStream:
cap = cv2.VideoCapture(0)

#now to the algorithm itself:
#we use Haar-Cascade and Tal Hassner method to get relavant roi's (region of interest) in the face
#every landmark (eye) is represented by 6 roi points: 2 upper points(a), 2 lower points(b) and 2 horizontal points(c1, c2).

#calculate at every frame :
# 1. 2 * the average distance between a and b (vertical distance)
# 2. the max distance calculated above for every frame
# 3. the distance between c1 and c2 (horizontal distance)

# The algorithm goes as follows:
# divide bullets .1/.3 and .2/.3 to get a normalized size (The 2nd bullet calculates the max normalized size)
# check if that value calculated above is smaller then a certain treshold (eyes are closed)
# if so - check if that situation does not change for a certain amount of time (time treshold- can be determined by the user)
# if (during that time) the eyes are closed for more than a certain percentage (accuracy treshold) - alert!

max_right_distance = 0
max_left_distance = 0

first_upper_right_eye = 0
first_lower_right_eye = 0

first_upper_left_eye = 0
first_lower_left_eye = 0

second_upper_right_eye = 0
second_lower_right_eye = 0

second_upper_left_eye = 0
second_lower_left_eye = 0

right_eye_distance = 0
left_eye_distance = 0

in_right_horizontal = 0
out_right_horizontal = 0

in_left_horizontal = 0
out_left_horizontal = 0

right_horizontal = 0
left_horizontal = 0

start = 0
elapsed = 0

# optimal_sleep turns 'True' when detected a possible sleeping driver
# when in 'optional_sleep' mode begin the following process:
# 1. start timer
# 2. count number of frames when a closed eye have been detected
# 3. count number of frames in total
# 4. when a number_of_seconds has passed:
#    a. if the ratio between bullets 2 and 3 above is greater then a treshold, alert the user
#    b. else - initialize the variables to the default situation

optional_sleep = False
closed_eye = 0
frames = 0
alert = 0

def get_landmarks(im):
    # get the face landmark points
    rects = face_cascade.detectMultiScale(im, 1.3, 5)
    x, y, w, h = rects[0]
    rect = dlib.rectangle(x, y, x + w, y + h)
    return numpy.matrix([[p.x, p.y] for p in predictor(im, rect).parts()])

def annotate_landmarks(im, landmarks):
    # number each point and present it
    im = im.copy()
    for idx, point in enumerate(landmarks):
        #annotate only the relavant regions - the landmark points of the eyes
        if ( (idx == 36) or (idx == 37) or (idx == 38) or (idx == 39) or (idx == 40) or (idx == 41) or (idx == 42) or
                 (idx == 43) or (idx == 44) or (idx == 45) or (idx == 46) or (idx == 47) ):
            pos = (point[0, 0], point[0, 1])
            cv2.putText(im, str(idx), pos,
                        fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                        fontScale=0.4,
                        color=(0, 0, 255))
            cv2.circle(im, pos, 3, color=(0, 255, 255))

        # find the relevant landmark for every roi:
        if (idx == 36):
            global out_right_horizontal
            out_right_horizontal = pos
        elif (idx == 37):
            global second_upper_right_eye
            second_upper_right_eye = pos
        elif (idx == 38):
            global first_upper_right_eye
            first_upper_right_eye = pos
        elif (idx == 39):
            global in_right_horizontal
            in_right_horizontal = pos
        elif (idx == 40):
            global first_lower_right_eye
            first_lower_right_eye = pos
        elif (idx == 41):
            global second_lower_right_eye
            second_lower_right_eye = pos
        elif (idx == 42):
            global in_left_horizontal
            in_left_horizontal = pos
        elif (idx == 43):
            global first_upper_left_eye
            first_upper_left_eye = pos
        elif (idx == 44):
            global second_upper_left_eye
            second_upper_left_eye = pos
        elif (idx == 45):
            global out_left_horizontal
            out_left_horizontal = pos
        elif (idx == 46):
            global second_lower_left_eye
            second_lower_left_eye = pos
        elif (idx == 47):
            global first_lower_left_eye
            first_lower_left_eye = pos
    return im

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        #when Haarr-Cascade has found a face:
        landmarks = get_landmarks(img)
        img = annotate_landmarks(img, landmarks)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

    # calculate the distance for every eye:

        # calculate the horizontal distance for each eye
        right_horizontal = math.hypot(in_right_horizontal[0] - out_right_horizontal[0],
                                    in_right_horizontal[1] - out_right_horizontal[1])

        left_horizontal = math.hypot(in_left_horizontal[0] - out_left_horizontal[0],
                                    in_left_horizontal[1] - out_left_horizontal[1])

        # calculate the 2 vertical distances in the right eye
        first_right_distance = math.hypot(first_upper_right_eye[0] - first_lower_right_eye[0],
                                        first_upper_right_eye[1] - first_lower_right_eye[1])

        second_right_distance = math.hypot(second_upper_right_eye[0] - second_lower_right_eye[0],
                                        second_upper_right_eye[1] - second_lower_right_eye[1])

        # calculate the 2 certical distances in the left eye
        first_left_distance = math.hypot(first_upper_left_eye[0] - first_lower_left_eye[0],
                                         first_upper_left_eye[1] - first_lower_left_eye[1])

        second_left_distance = math.hypot(second_upper_left_eye[0] - second_lower_left_eye[0],
                                          second_upper_left_eye[1] - second_lower_left_eye[1])

        # calculate the final normalized distance for each eye
        right_eye_distance = (first_right_distance + second_right_distance) / (2 * ((float)(right_horizontal)))
        left_eye_distance = (first_left_distance + second_left_distance) / (2 * ((float)(left_horizontal)))

        # calculate the max distance for every eye
        max_right_distance = max(right_eye_distance, max_right_distance)
        max_left_distance = max(left_eye_distance, max_left_distance)

        # handle false max_distance calculation - if the distance is bigger then a certain value ignore that frame sample:
        #if (max_right_distance > 0.8):
        #    max_right_distance = right_eye_distance
        #if (max_left_distance > 0.8):
        #    max_left_distance = left_eye_distance

        # check if both eyes are closed (the distance differences for each eye is smaller then the treshold):
        if ((left_eye_distance / (float)(max_left_distance)) < 0.5) and ((right_eye_distance / (float)(max_right_distance)) < 0.5):
            # start the clock only when the process begins
            if (not (optional_sleep)):
                start = time.clock()
                optional_sleep = True
            # count number of eyes closed
            closed_eye += 1
            # count number of frames
        if (start > 0):
            # test the time passed from the start
            elapsed = (time.clock() - start)
            frames += 1

        # if the time passed the time treshold and the accuracy is as wanted:
        if (elapsed > number_of_seconds):
            if (closed_eye / (float)(frames) > 0.7):
                #alert the user exactly one time:
                if (alert == 0):
                    print("Alert!!!")
                    # if the user would like to see the process, play the chosen music and also close the window.
                    # when the alert sound has finished - restart the system
                    if (show == True):
                        cv2.destroyAllWindows()
                        winsound.PlaySound(music, winsound.SND_FILENAME)
                    alert += 1

            else:
                # false detection - initialize all variables to the default state
                start = 0
                elapsed = 0
                closed_eye = 0
                frames = 0
                optional_sleep = False
                alert = 0

        #   optional - show a rectangle around the eyes if found by Haar - Cascade method:

        #eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        #show the process (depends on the user's choice):
        if (show):
            cv2.imshow('img', img)

    #close the program by clicking the 'esc' button
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
