#include "minibot.h"

// Create Minibot instance with your robot ID
Minibot robot("myRobot");

void setup() 
{
  Serial.begin(115200);
  robot.begin();
}

void loop() {
  // Get current time in milliseconds
  unsigned long currentTime = millis();
  
  // Calculate position in 8-second cycle
  unsigned long cycleTime = currentTime % 8000;
  
  float speed;
  
  if (cycleTime < 1000) {
    // 0-1s: Hold at neutral
    speed = 0.0;
  } 
  else if (cycleTime < 2000) {
    // 1-2s: Ramp up to full speed backward (0 to -1)
    unsigned long rampTime = cycleTime - 1000;
    speed = -(rampTime / 1000.0);
  } 
  else if (cycleTime < 3000) {
    // 2-3s: Hold full speed backward
    speed = -1.0;
  } 
  else if (cycleTime < 4000) {
    // 3-4s: Ramp down to neutral (-1 to 0)
    unsigned long rampTime = cycleTime - 3000;
    speed = -1.0 + (rampTime / 1000.0);
  } 
  else if (cycleTime < 5000) {
    // 4-5s: Hold at neutral
    speed = 0.0;
  } 
  else if (cycleTime < 6000) {
    // 5-6s: Ramp up to full speed forward (0 to 1)
    unsigned long rampTime = cycleTime - 5000;
    speed = (rampTime / 1000.0);
  } 
  else if (cycleTime < 7000) {
    // 6-7s: Hold full speed forward
    speed = 1.0;
  } 
  else {
    // 7-8s: Ramp down to neutral (1 to 0)
    unsigned long rampTime = cycleTime - 7000;
    speed = 1.0 - (rampTime / 1000.0);
  }
  
  // Drive the left motor
  Serial.println(speed);
  robot.driveLeftMotor(speed);
  
  // Small delay for stability
  delay(10);
}
