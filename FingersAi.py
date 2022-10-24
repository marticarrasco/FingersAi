import cv2
import mediapipe as mp
import math
import HandTrackingModule as htm
import keyboard
import serial

'''
sudo needed for this project in MacOs
ls /dev/tty.*   -- to find serial ports on MacOs
'''

cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

arduino = serial.Serial(port='/dev/tty.usbmodem14101', baudrate=9600, timeout=.1)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        fingers1 = detector.fingersUp(hand1)
        
        dataToSend = "$"+str(int(fingers1[0]))+str(int(fingers1[1]))+str(int(fingers1[2]))+str(int(fingers1[3]))+str(int(fingers1[4]))
        try:
            arduino.write(bytes(dataToSend, 'utf-8'))
            print(dataToSend)
        except:
            pass

        cv2.putText(img,str(dataToSend),(20, 30),cv2.FONT_HERSHEY_PLAIN,
                                    2,(0, 0, 0),2)
    else:
        cv2.putText(img,"HAND NOT RECOGNIZED",(20, 30),cv2.FONT_HERSHEY_PLAIN,
                                    2,(0, 0, 0),2)

    if keyboard.is_pressed("q"):
        break
        
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
