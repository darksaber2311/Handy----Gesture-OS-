# PHASE 3 -- we gonna move our cursor with hand gestures
import cv2
import mediapipe as mp
import pyautogui

screen_width, screen_height  = pyautogui.size()
print(screen_width, screen_height)

#pyautogui.moveTo(100,1000)


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    #
)

# Drawing utilities
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("hand Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("hand Tracking",1000, 800)


prev_x,prev_y = 0,0
smoothening = 5
while True : 
    success,frame  = cap.read()
    if(not success):
        break
    frame = cv2.flip(frame,1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            fingers = []
            if(hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x):
                fingers.append(1)
            else:
                fingers.append(0)
            if(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y):
                fingers.append(1)
            else:
                fingers.append(0)
            if(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y):
                fingers.append(1)
            else:
                fingers.append(0)
            if(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y):
                fingers.append(1)
            else:
                fingers.append(0)
            if(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y):
                fingers.append(1)
            else:
                fingers.append(0)


            if(fingers == [0,1,0,0,0]):
                h,w,c = frame.shape
                cx = int(hand_landmarks.landmark[8].x * w)
                cy = int(hand_landmarks.landmark[8].y * h)

               
                cv2.circle(frame,(cx,cy),10,(255,0,255),cv2.FILLED)
                screen_x = int(cx/w * screen_width)
                screen_y = int(cy/h * screen_height)
                curr_x = prev_x + (screen_x - prev_x)/smoothening
                curr_y = prev_y +(screen_y - prev_y)/smoothening 
                pyautogui.moveTo(curr_x,curr_y)
                prev_x,prev_y = curr_x, curr_y

    cv2.imshow("hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()    


