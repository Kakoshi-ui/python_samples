import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils # type: ignore
mp_hands = mp.solutions.hands # type: ignore

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.8) as hands:

    while (1):
        ret, frame = cap.read()
        if ret == False :
            break
            pass
        heigh, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                pass
            pass

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
            pass
        pass
cap.release()
cv2.destroyAllWindows()