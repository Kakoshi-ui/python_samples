import cv2
from ultralytics import YOLO
import hand_track as ht
import audio
import serial

#instanciating the webcam and adjusting it
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

#reading cnn
model = YOLO('best.pt')

#audio controller:
media_controller = audio.AudioController()

#Arduino serial data
arduino_uno = serial.Serial(port='COM3', baudrate=9600)

#instance for the hand detection object
detector = ht.hand_detector()

out_label = ""
to_arduino = ''
audio_opt = 0

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
        xmin = xmin - 20
        ymin = ymin - 20
        xmax = xmax + 20
        ymax = ymax + 20

        # Capturing info
        cap_cut = frame[ymin:ymax, xmin:xmax]

        #Resizing
        cap_cut = cv2.resize(cap_cut, (640, 640), interpolation=cv2.INTER_CUBIC)

        results = model.predict(cap_cut, conf=0.8)
        labels = model.names

        if len(results) != 0:
            for evry_res in results:
                masks = evry_res.masks
                coord = masks

                ann = results[0].plot()

                for c in evry_res.boxes.cls:
                    out_labels = labels[int(c)]
                    
                    if out_labels == "Play":
                        audio_opt = 0
                        to_arduino = '0'
                    elif out_labels == "Pause":
                        audio_opt = 1
                        to_arduino = '1'
                    elif out_labels == "V+":
                        audio_opt = 2
                        to_arduino = '2'
                    elif out_labels == "V-":
                        audio_opt = 3
                        to_arduino = '3'
                    else:
                        audio_opt = 4
                        to_arduino = '4'
                    media_controller.vol_control(audio_opt)
                    arduino_uno.write(to_arduino.encode())

                pass
            pass
        cv2.imshow("cut", ann)
        pass
    
    cv2.imshow("Video", frame)
    t = cv2.waitKey(1)
    if t == 27:
        break
    pass

cap.release()
cv2.destroyAllWindows()