import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Set up serial communication with Arduino
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Ensure the port is correct
    time.sleep(2)  # Give time for the serial connection to establish
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    arduino = None

# Open camera
cap = cv2.VideoCapture(0)


def map_finger_to_servo(y, img_height):
    """
    Maps the y-coordinate of a fingertip to a servo angle (0 to 180 degrees).

    Args:
        y (float): The normalized y-coordinate of the fingertip (0.0 to 1.0).
        img_height (int): The height of the image/frame.

    Returns:
        int: The corresponding servo angle (0 to 180 degrees).
    """
    # Convert normalized y to pixel value
    y_pixel = y * img_height

    # Map y_pixel to a servo angle (0 to 180 degrees)
    # Assuming top of the frame corresponds to 0 degrees and bottom to 180 degrees
    servo_angle = int((1 - y_pixel / img_height) * 180)

    # Clip to valid range
    servo_angle = max(0, min(servo_angle, 180))

    return servo_angle


previous_angle = None

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the index fingertip landmark
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Map the y-coordinate of the fingertip to a servo angle
            angle = map_finger_to_servo(index_tip.y, img.shape[0])

            # Send the command only if the angle has changed
            if angle != previous_angle and arduino:
                arduino.write(f'{angle}\n'.encode())
                print(f"Servo angle: {angle}")
                previous_angle = angle

    cv2.imshow("Finger Gesture Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.close()
