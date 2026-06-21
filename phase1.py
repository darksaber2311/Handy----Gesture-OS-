import cv2
import mediapipe as mp

#Phase1

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Drawing utilities
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Index finger tip = landmark 8
            h, w, c = frame.shape

            index_tip = hand_landmarks.landmark[8]

            cx = int(index_tip.x * w)
            cy = int(index_tip.y * h)

            # Draw circle on index finger tip
            cv2.circle(frame, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            # Display coordinates
            cv2.putText(
                frame,
                f"X:{cx} Y:{cy}",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            print(f"Index Finger -> X:{cx}, Y:{cy}")

    cv2.imshow("GestureOS - Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()