#include "minibot.h"

// Create your robot (put your name here!)
Minibot bot("minibot_ex");

float left = 0.0;
float right = 0.0;

void setup() {
  // Initialize the robot - runs once at startup
  bot.begin();
}

void loop() {
  // Update controller values - ALWAYS FIRST!
  bot.updateController(); 

  if (bot.getGameStatus() == "standby") {
    bot.stopAllMotors();
  }
  else {
    left = (bot.getLeftY() < 130 && bot.getLeftY() > 125) ? 0.0 : -1*(bot.getLeftY()) / 128.0 + 1;
    right = (bot.getRightY() < 130 && bot.getRightY() > 125) ? 0.0 : -1*(bot.getRightY()) / 128.0 + 1;
    Serial.println("Left: " + String(left));
    Serial.println("Right: " + String(right));
    bot.driveLeftMotor(left);
    bot.driveRightMotor(right);
  }
}