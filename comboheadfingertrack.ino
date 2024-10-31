#include <Servo.h>

Servo servoHorizontal;  // Horizontal servo object
Servo servoVertical;    // Vertical servo object
Servo myServo;          // Generic servo object

int servoHorizontalPin = 9;  // Pin for horizontal servo
int servoVerticalPin = 10;   // Pin for vertical servo
int myServoPin = 11;         // Pin for the generic servo (optional)

void setup() {
  Serial.begin(9600);  // Start serial communication
  
  // Attach the servos to their respective pins
  servoHorizontal.attach(servoHorizontalPin);
  servoVertical.attach(servoVerticalPin);
  myServo.attach(myServoPin);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the incoming data until newline
    int commaIndex = data.indexOf(',');          // Find the position of the comma

    if (commaIndex == -1) {
      // No comma detected, assume single-servo mode (generic servo)
      int angle = data.toInt();  // Convert the string to an integer
      
      // Move the generic servo to the specified angle
      if (angle >= 0 && angle <= 180) {
        myServo.write(angle);
        Serial.print("Generic Servo Angle: ");
        Serial.println(angle);
      }
      
    } else {
      // Comma detected, assume horizontal and vertical servo mode
      int horizontalAngle = data.substring(0, commaIndex).toInt();  // Parse horizontal angle
      int verticalAngle = data.substring(commaIndex + 1).toInt();   // Parse vertical angle

      // Debugging: Print the angles to the serial monitor
      Serial.print("Horizontal Angle: ");
      Serial.println(horizontalAngle);
      Serial.print("Vertical Angle: ");
      Serial.println(verticalAngle);

      // Move the horizontal servo
      if (horizontalAngle >= 0 && horizontalAngle <= 180) {
        servoHorizontal.write(horizontalAngle);
      }

      // Move the vertical servo
      if (verticalAngle >= 0 && verticalAngle <= 180) {
        servoVertical.write(verticalAngle);
      }
    }

    delay(20);  // Wait for the servos to reach the positions
  }
}
