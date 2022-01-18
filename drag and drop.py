import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import pyfirmata

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("Camera couldn't access")
    exit()

detector = HandDetector(detectionCon=0.7)

port = "COM7"
board = pyfirmata.Arduino(port)
servo_pinX = board.get_pin('d:5:s') #pin 5 Arduino
servo_pinY = board.get_pin('d:6:s') #pin 6 Arduino

x, y = 150, 230
w, h = 200, 200
col  = (255, 0, 255)

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    servoX = np.interp(x, [0, 1280], [0, 180])
    servoY = np.interp(y, [0, 720], [0, 180])

    if lmList:
        dist,_,_ = detector.findDistance(8, 12, img, draw = False)
        #print(dist)
        fingers = detector.fingersUp()
        if fingers[1] == 1 and fingers[2] == 1:
            cursor = lmList[8]
            if dist < 50:
                if x-w // 2 < cursor[0] < x+w-120 // 2 and y-h // 2 < cursor[1] < y+h-120 // 2:
                    col = (255, 255, 0)
                    x, y = cursor
                cv2.circle(img, cursor, 50, (255, 255, 0), cv2.FILLED)
                cv2.putText(img, "HOLD", (cursor[0]-40, cursor[1]), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255), 2)

            else:
                col = (255, 0, 255)


    cv2.rectangle(img, (x-w // 2, y-h // 2), (x+w // 2, y+h // 2), col, cv2.FILLED)
    cv2.putText(img, f'({str(x)}, {str(y)})', (x-90, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
    cv2.rectangle(img, (40,20), (350,110), (0,255,255), cv2.FILLED)
    cv2.putText(img, f'Servo X: {int(servoX)} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servoY)} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    servo_pinX.write(servoX)
    servo_pinY.write(servoY)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

