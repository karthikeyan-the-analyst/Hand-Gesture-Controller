import cv2
import mediapipe as mp
import pyautogui
import keyboard  # type: ignore

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Try to open webcam
cap = cv2.VideoCapture(0)  # You can try 1 or 2 if 0 doesn't work
if not cap.isOpened():
    print("❌ Error: Cannot access camera on index 0. Try index 1 or 2.")
    exit()

def count_fingers(hand_landmarks):
    """Count extended fingers using landmark positions."""
    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    finger_tips = [8, 12, 16, 20]
    finger_bottoms = [6, 10, 14, 18]

    for tip, bottom in zip(finger_tips, finger_bottoms):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[bottom].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Warning: Failed to read from camera.")
        break

    # Flip for natural movement
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            finger_count = count_fingers(hand_landmarks)

            if finger_count == 0:  # Closed fist (Brake)
                keyboard.release("right")
                keyboard.press("left")
                print("Brake Pressed")
            elif finger_count == 2:  # Two fingers up (Reverse)
                keyboard.release("right")
                keyboard.press("down")  # Assuming "down" is reverse
                print("Reverse Pressed")
            elif finger_count == 1:  # Thumb only (Flip maybe)
                keyboard.press("space")  # Example: for stunts or flip
                print("Flip / Stunt")
            elif finger_count == 5:  # All fingers (Gas)
                keyboard.release("left")
                keyboard.press("right")
                print("Gas Pressed")
            else:
                keyboard.release("right")
                keyboard.release("left")
                keyboard.release("down")
                keyboard.release("space")


    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
