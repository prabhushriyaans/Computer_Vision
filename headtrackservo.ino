#include <Servo.h>

Servo servoHorizontal;
Servo servoVertical;
int servoHorizontalPin = 9;
int servoVerticalPin = 10;

void setup() {
  Serial.begin(9600);  // Start serial communication
  servoHorizontal.attach(servoHorizontalPin);  // Attach the horizontal servo to pin 9
  servoVertical.attach(servoVerticalPin);      // Attach the vertical servo to pin 10
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the incoming data until newline
    int commaIndex = data.indexOf(',');          // Find the position of the comma

    // Check if the comma was found, if not, skip
    if (commaIndex == -1) return;

    // Split the data into horizontal and vertical angles
    int horizontalAngle = data.substring(0, commaIndex).toInt();  // Parse horizontal angle
    int verticalAngle = data.substring(commaIndex + 1).toInt();   // Parse vertical angle

    // Debugging: Print the angles to the serial monitor
    Serial.print("Horizontal Angle: ");
    Serial.println(horizontalAngle);
    Serial.print("Vertical Angle: ");
    Serial.println(verticalAngle);

    // Move the servos to the specified angles
    if (horizontalAngle >= 0 && horizontalAngle <= 180) {
      servoHorizontal.write(horizontalAngle);  // Set horizontal servo
    }
    
    if (verticalAngle >= 0 && verticalAngle <= 180) {
      servoVertical.write(verticalAngle);      // Set vertical servo
    }

    delay(20);  // Wait for the servos to reach the positions
  }
}
