import cv2
from cvzone.PoseModule import PoseDetector
#from cvzone.FaceMeshModule import FaceMeshDetector


#cap = cv2.VideoCapture(0)


cap = cv2.VideoCapture()
cap.open('a.mp4')
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

detector = PoseDetector()
first = 0
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
    first = first + 1
    if first == 10:
        for id, lm in enumerate(lmList):
            print(lm)


     # img = cv2.resize(img, (1280, 720)) 
    cv2.imshow("Image", img)
    cv2.waitKey(1)
