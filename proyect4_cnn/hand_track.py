#File created using mediapipe for tracking the hand position, init mediapipe and other functions
#Code taken from the chanel: Aprende e Ingenia. URL: https://www.youtube.com/watch?v=8cbCruS5Z-E&t=405s
#thank you for your work
import math
import cv2
import mediapipe as mp
import time

class hand_detector():
    #function __init__: begin with the parameters to instanciate the object from mediapipe to track hands using the webcam
    def __init__(self, mode=False, maxHands=1, model_complexity=1, conf_detection=0.9, conf_sef=0.6):
        self.mode = mode
        self.max_hands = maxHands
        self.compl = model_complexity
        self.conf_detection = conf_detection
        self.conf_sef = conf_sef

        self.mp_hands = mp.solutions.hands # type: ignore
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.compl, self.conf_detection, self.conf_sef)
        self.draw = mp.solutions.drawing_utils # type: ignore
        self.tip = [4, 8, 12, 20]
        pass

    def find_hands(self, frame, drawing=True):

        #This method uses mediapipe to track the 21 hand landmarks and drawing it in the image, in this case we're using the webcam

        image_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_color)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if drawing:
                    self.draw.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
                    pass
                pass
            pass
        pass
        return frame
    pass

    def find_position(self, frame, hand_num=0, draw_point=True, draw_box=True, color=[]):
        x_list = []
        y_list = []
        bbox = []
        player = 0
        self.list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]
            test = self.results.multi_hand_landmarks
            player = len(test)
            for id, lm in enumerate(my_hand.landmark):
                height, width, _ = frame.shape
                cx, cy = int(lm.x * width), int(lm.y* height)
                x_list.append(cx)
                y_list.append(cy)
                self.list.append([id, cx, cy])
                if draw_point:
                    cv2.circle(frame, (cx, cy), 3, (0,0,0), cv2.FILLED)
                    pass
                pass
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = xmin, ymin, xmax, ymax
            if draw_box:
                cv2.rectangle(frame, (xmin-20, ymin-20), (xmax+20, ymax+20), color, 2)
                pass
            pass
        return self.list, bbox, player
        pass

    def finger_up(self):
        finger = []
        if self.list[self.tip[0]][1] > self.list[self.tip[0]-1][1]:
            finger.append(1)
            pass
        else:
            finger.append(0)
            pass
        for id in range (1, 5):
            if self.list[self.tip[id]][2] < self.list[self.tip[id]-2][2]:
                finger.append(1)
                pass
            else:
                finger.append(0)
                pass
            pass
        return finger
        pass

    def distance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (0,0,255), t)
            cv2.circle(frame, (x1,y1), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (x2,y2), r, (0,0,255), cv2.FILLED)
            cv2.circle(frame, (cx,cy), r, (0,0,255), cv2.FILLED)
            pass
        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]
        pass

def main():
    ptime = 0
    ctime = 0

    cap = cv2.VideoCapture(0)
    detector = hand_detector()

    while (1):
        ret, frame = cap.read()
        frame = detector.find_hands(frame)

        s_list, bbox, _ = detector.find_position(frame)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(frame, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        k = cv2.waitKey(1)

        if k == 27:
            break
            pass
        pass
    cap.release()
    cv2.destroyAllWindows()
    pass

if __name__ == "__main__":
    main()
    pass
