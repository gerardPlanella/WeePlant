import numpy as np
import face_recognition
import time
import math
import cv2
import os
from keras.preprocessing import image
from keras.models import model_from_json

FRAME_R = 300
FRAME_L = 100

class Person():
    __slots__ = ("name", "image", "encoding")


    def __init__ (self, name):
        if name != None:
            self.name = name
            self.image = face_recognition.load_image_file("faces/" + name + ".jpg")
            self.encoding = face_recognition.face_encodings(self.image)[0]


    def getName(self):
        return self.name

    def getEncoding(self):
        return self.encoding

def anyoneInCamera():
    video_capture = cv2.VideoCapture(0)

    # Grab a single frame of video
    ret, frame = video_capture.read()

    #We are done with the webcam.
    video_capture.release()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)

    cv2.imshow('img',frame)

    return len(face_locations) != 0

def recognize_face(frame_detect_number):
    FRAME_DETECT_NUMBER = frame_detect_number

    known_face_encodings = []
    known_face_names = []
    people = []

    video_capture = cv2.VideoCapture(0)


    f = open("faces/face_names.txt", "r")
    f_parser = f.readlines()

    i = 0
    if f_parser != None:
        for name in f_parser:
            if name != "\n":
                aux = name.strip('\n')
                people.append(Person(name = aux))
                known_face_names.append(people[i].getName())
                known_face_encodings.append(people[i].getEncoding())
                i = i + 1

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    done = False
    detected_frames = 0
    face_picture = 0

    print(str(people))
    print(str(known_face_names))

    while not done:

        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

            if (len(face_encodings) > 0) :
                face_names.append(name)
                detected_frames = detected_frames + 1

            if detected_frames >= FRAME_DETECT_NUMBER:
                face_picture = frame
                break

        process_this_frame = not process_this_frame

    # Release handle to the webcam
    video_capture.release()
    f.close()
    return (face_names[0], face_picture)

def waitForEmotion(emotion_input, max_val):

    MAX_EMOTION = max_val
    emotion_cnt = 0
    #-----------------------------
    #opencv initialization

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    #-----------------------------

    #face expression recognizer initialization

    model = model_from_json(open("facial_expression_model_structure.json", "r").read())
    model.load_weights('facial_expression_model_weights.h5') #load weights
    #-----------------------------

    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    if emotion_input not in emotions:
        return -1

    while(True):
        ret, img = video_capture.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)#finds faces in frame


        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image

            detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis = 0)

            img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

            predictions = model.predict(img_pixels) #store probabilities of 7 expressions

            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
            max_index = np.argmax(predictions[0])

            emotion = emotions[max_index]

            #write emotion text above rectangle
            cv2.putText(img, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

            if emotion_input == emotion:
                emotion_cnt = emotion_cnt + 0.5
            elif emotion_cnt > 0:
                emotion_cnt = emotion_cnt - 1

            #process on detected face end
            #-------------------------

        cv2.imshow('img',img)

        if emotion_cnt >= MAX_EMOTION:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'): # Hit 'q' on the keyboard to quit!
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return 0


def recognize_gesture(gesture_number, gesture_limit):
    cap = cv2.VideoCapture(0)
    finger_cnt = 0
    time.sleep(.5)
    while(1):


        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
        #define region of interest
        roi=frame[FRAME_L:FRAME_R, FRAME_L:FRAME_R]


        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # define range of skin color in HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)

     #extract skin colur image
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
    #extrapolate the hand to fill dark spots within
        mask = cv2.dilate(mask,kernel,iterations = 4)

    #blur the image
        mask = cv2.GaussianBlur(mask,(5,5),100)
    #find contours
        (contours, _) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            continue;

   #find contour of max area(hand)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
    #approx the contour a little
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
    #make convex hull around hand
        hull = cv2.convexHull(cnt)

     #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)

    #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100

     #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        l=0

        if defects is not None:
    # l = no. of defects

    #code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt= (100,180)


                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                s = (a+b+c)/2
                ar = math.sqrt(s*(s-a)*(s-b)*(s-c))

                #distance between point and convex hull
                d=(2*ar)/a

                # apply cosine rule here
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57


                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d>30:
                    l += 1
                    cv2.circle(roi, far, 3, [255,0,0], -1)

                #draw lines around hand
                cv2.line(roi,start, end, [0,255,0], 2)


        l+=1

        if l >= gesture_number:
            finger_cnt+=1
        elif finger_cnt > 0:
            finger_cnt-=1

        if finger_cnt == gesture_limit:
            break;



        #print corresponding gestures which are in their ranges
        font = cv2.FONT_HERSHEY_SIMPLEX
        if l==1:
            if areacnt<2000:
                cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            else:
                if arearatio<12:
                    cv2.putText(frame,'0',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                elif arearatio<17.5:
                    cv2.putText(frame,'Best of luck',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

                else:
                    cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        elif l==2:
            cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        elif l==3:

              if arearatio<27:
                    cv2.putText(frame,'3',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
              else:
                    cv2.putText(frame,'ok',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        elif l==4:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        elif l==5:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        else :
            cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)

        #show the windows
        cv2.imshow('mask',mask)
        cv2.imshow('frame',frame)



        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
