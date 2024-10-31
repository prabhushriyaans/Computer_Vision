#include <Servo.h>

Servo myServo;
int servoPin = 9;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');  // Read the incoming data
    int angle = data.toInt();  // Convert the string to an integer

    // Move the servo to the specified angle
    myServo.write(angle);
    delay(20);  // Wait for the servo to reach the position
  }
}
