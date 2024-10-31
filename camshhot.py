import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

photo_counter = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Convert the frame to RGB for hand detection
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Accessing landmark 4 (Thumb tip) and 8 (Index fingertip) to detect a pinch gesture
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Calculate the distance between the thumb and index fingertip
                thumb_coords = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))
                index_finger_coords = (int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0]))
                distance = ((thumb_coords[0] - index_finger_coords[0]) ** 2 + (thumb_coords[1] - index_finger_coords[1]) ** 2) ** 0.5

                # If the distance is below a threshold, consider it as a gesture for taking a picture
                if distance < 40:  # Adjust the threshold as necessary
                    photo_counter += 1
                    photo_filename = f"photo_{photo_counter}.jpg"
                    cv2.imwrite(photo_filename, frame)
                    print(f"Photo taken: {photo_filename}")

        # Display the resulting frame
        cv2.imshow('Camera Feed', frame)

        # Press 'q' to exit the loop and close the camera
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error: Failed to capture image.")
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
hands.close()
