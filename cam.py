import cv2

# Open the camera
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame reading was successful
    if ret:
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
