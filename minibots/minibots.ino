#include "minibot.h"

// Create minibot object with robot ID and motor pins
// Preferred motor pins: left=16, right=17, dcMotor=18, servoMotor=19
Minibot bot("Sample Robot");

void setup() {
  bot.begin();
}

void loop() {
  // Update controller values from the remote
  bot.updateController();

  // TODO: Write your robot control code here
  if (bot.GetGameStatus() == "teleop"){
    //This is Tank Drive which means each joystick controls that side's respective motor
    float leftSpeed = (bot.getLeftY() - 127.5) / 127.5;//Speed is proportional to how far you move joystick.
    float rightSpeed = (bot.getRightY() - 127.5) / 127.5;
    bot.driveLeftMotor(leftSpeed);
    bot.driveRightMotor(rightSpeed);

    //Servo motors for manipulator use
    if (bot.getSquare()) {
      bot.driveServoMotor(-30);//Turn motor left
    } 
    else if (bot.getTriangle()) {
      bot.driveServoMotor(30);//right
    }
    else {
      bot.driveServoMotor(0);//center
    }
  } 
}