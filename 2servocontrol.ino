#include <Servo.h>

Servo myServo1;  // First servo object
Servo myServo2;  // Second servo object

int servoPin1 = 9;   // Pin for the first servo
int servoPin2 = 10;  // Pin for the second servo

void setup() {
  Serial.begin(9600);
  
  myServo1.attach(servoPin1);  // Attach the first servo to pin 9
  myServo2.attach(servoPin2);  // Attach the second servo to pin 10
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the incoming data
    
    // Split the incoming string data for both servos
    int commaIndex = data.indexOf(',');  // Find the comma separator between two angles
    String angle1Str = data.substring(0, commaIndex);  // First part before the comma
    String angle2Str = data.substring(commaIndex + 1);  // Second part after the comma
    
    int angle1 = angle1Str.toInt();  // Convert the first part to an integer (for servo 1)
    int angle2 = angle2Str.toInt();  // Convert the second part to an integer (for servo 2)

    // Move both servos to their respective angles
    myServo1.write(angle1);
    myServo2.write(angle2);

    delay(20);  // Wait for the servos to reach their positions
  }
}
