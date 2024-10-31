import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Face Mesh connections need to be imported separately
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh_connections = mp_face_mesh.FACEMESH_TESSELATION  # Using face mesh tesselation for drawing

# Set up serial communication with Arduino
try:
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Ensure the port is correct
    time.sleep(2)  # Give time for the serial connection to establish
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    arduino = None

# Open camera
cap = cv2.VideoCapture(0)


def map_position_to_servo(x, y, img_width, img_height):
    """
    Maps the x and y coordinates of a head position to two servo angles (0 to 180 degrees for both).

    Args:
        x (float): The normalized x-coordinate of the landmark (0.0 to 1.0).
        y (float): The normalized y-coordinate of the landmark (0.0 to 1.0).
        img_width (int): The width of the image/frame.
        img_height (int): The height of the image/frame.

    Returns:
        tuple: Corresponding servo angles for horizontal (azimuth) and vertical (elevation) movement (0 to 180 degrees).
    """
    # Convert normalized x and y to pixel values
    x_pixel = x * img_width
    y_pixel = y * img_height

    # Map x_pixel and y_pixel to servo angles (0 to 180 degrees)
    # Assuming left of the frame corresponds to 0 degrees and right to 180 degrees for horizontal movement
    # Top of the frame corresponds to 0 degrees and bottom to 180 degrees for vertical movement
    servo_horizontal = int((x_pixel / img_width) * 180)  # Horizontal angle (left-right)
    servo_vertical = int((1 - y_pixel / img_height) * 180)  # Vertical angle (up-down)

    # Clip to valid range
    servo_horizontal = max(0, min(servo_horizontal, 180))
    servo_vertical = max(0, min(servo_vertical, 180))

    return servo_horizontal, servo_vertical


previous_horizontal_angle = None
previous_vertical_angle = None

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw the face mesh landmarks with tesselation
            mp_draw.draw_landmarks(
                img,
                face_landmarks,
                mp_face_mesh_connections,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # Get the tip of the nose landmark (index 1 in the face mesh)
            nose_tip = face_landmarks.landmark[1]

            # Map the x and y coordinates of the nose tip to servo angles
            horizontal_angle, vertical_angle = map_position_to_servo(
                nose_tip.x, nose_tip.y, img.shape[1], img.shape[0]
            )

            # Send the command only if the angles have changed
            if (horizontal_angle != previous_horizontal_angle or vertical_angle != previous_vertical_angle) and arduino:
                arduino.write(f'{horizontal_angle},{vertical_angle}\n'.encode())
                print(f"Servo angles: Horizontal = {horizontal_angle}, Vertical = {vertical_angle}")
                previous_horizontal_angle = horizontal_angle
                previous_vertical_angle = vertical_angle

    cv2.imshow("Head Movement Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if arduino:
    arduino.close()