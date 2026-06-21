import cv2
import mediapipe as mp
from numpy import append

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

cap = cv2.VideoCapture(0);

#we are going to use the mediapipe library to detect fingers and their landmarks


while True:
    success, frame  = cap.read()

    if not success:
        break
    frame  = cv2.flip(frame,1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            '''if(hand_landmarks.landmark[8].y<hand_landmarks.landmark[6].y):
                print("Finger is up")
            else:
                print("Finger is down")
            if(hand_landmarks.landmark[4].x>hand_landmarks.landmark[3].x):
                print("Thumb is up")
            else:
                print("Thumb is down")    '''
            fingers = []
            #thumb
            if(hand_landmarks.landmark[4].x>hand_landmarks.landmark[3].x):
                fingers.append(1)
            else: 
                fingers.append(0)


            #index
            if(hand_landmarks.landmark[8].y<hand_landmarks.landmark[6].y):
                fingers.append(1)
            else: 
                fingers.append(0)

  
            #middle
            if(hand_landmarks.landmark[12].y<hand_landmarks.landmark[10].y):
                fingers.append(1)
            else: 
                fingers.append(0)

            #ring    
            if(hand_landmarks.landmark[16].y<hand_landmarks.landmark[14].y):
                fingers.append(1)
            else: 
                fingers.append(0)

            #pinky    
            if(hand_landmarks.landmark[20].y<hand_landmarks.landmark[18].y):
                fingers.append(1)
            else: 
                fingers.append(0)                                                                    
            gestures = ""
            if (fingers == [0,0,0,0,0]):
                gestures = "FIST"
            elif (fingers == [0,1,1,0,0,]):
                gestures = "PEACE"
            elif (fingers == [0,1,0,0,0]):
                gestures = "NERD"
            elif(fingers == [0,0,1,0,0]):
                gestures = "FK YOU"
            elif(fingers == [1,1,1,1,1]):
                gestures = "HIGH FIVE" 
            else :
                gestures = "Some bs"           
            cv2.putText(
                frame,
                gestures,
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )
    cv2.imshow("GestureOS - Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
