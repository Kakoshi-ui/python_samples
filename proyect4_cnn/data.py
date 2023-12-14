import cv2
import os
import hand_track as ht

#instanciating the webcam and adjusting it
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

folder = "C:\\Users\\axel9\\Documents\\Intelligent_Sys\\convolutional_net\\dataset\\pause\\"

#instance for the hand detection object
detector = ht.hand_detector()
counter = 0

while True:
    #capturing the video image
    ret, frame = cap.read()
    #tracking hand position in image
    frame = detector.find_hands(frame, drawing=False)

    list_1, bbox, hand = detector.find_position(frame, draw_point=False, draw_box=False, color=[0,0,255])

    if hand == 1:
        #extracting info from the frame
        xmin, ymin, xmax, ymax = bbox

        #Margin
        xmin = xmin - 40
        ymin = ymin - 40
        xmax = xmax + 40
        ymax = ymax + 40

        # Capturing info
        cap_cut = frame[ymin:ymax, xmin:xmax]

        #Resizing
        cap_cut = cv2.resize(cap_cut, (640, 640), interpolation=cv2.INTER_CUBIC)

        #saving images
        if counter <= 100:    
            cv2.imwrite(folder + "pause_{}.jpg".format(counter), cap_cut)
            cv2.imshow("Cut", cap_cut)
            counter = counter + 1
            pass
        pass

    cv2.imshow("detection", frame)

    t = cv2.waitKey(1)
    if t == 27:
        break
    pass

cap.release()
cv2.destroyAllWindows()