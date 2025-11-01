#include "minibot.h"

// Constructor
Minibot::Minibot(const char* robotId,
                 int leftMotorPin, int rightMotorPin,
                 int dcMotorPin, int servoMotorPin,
                 int leftMotorPwmOffset, int rightMotorPwmOffset,
                 int dcMotorPwmOffset)
                  : robotId(robotId),
                      leftMotorPin(leftMotorPin), rightMotorPin(rightMotorPin),
                      dcMotorPin(dcMotorPin), servoMotorPin(servoMotorPin),
                      leftMotorPwmOffset(leftMotorPwmOffset),
                      rightMotorPwmOffset(rightMotorPwmOffset),
                      dcMotorPwmOffset(dcMotorPwmOffset)
{
  
}

void Minibot::begin()
{
  Serial.begin(115200);
  ledcAttach(leftMotorPin, freq, resolution);
  ledcAttach(rightMotorPin, freq, resolution);
  ledcAttach(dcMotorPin, freq, resolution);
  ledcAttach(servoMotorPin, freq, resolution);

  // Wi-Fi connection
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  // Start UDP
  udp.begin(UDP_PORT);
  Serial.println("Listening on UDP port " + String(UDP_PORT));

  // Stop all motors initially
  stopAllMotors();
}


void Minibot::sendDiscoveryPing() {
  // Format: "DISCOVER:<robotId>:<IP>"
  String msg = "DISCOVER:" + String(robotId) + ":" + WiFi.localIP().toString();
  udp.beginPacket(IPAddress(255, 255, 255, 255), DISCOVERY_PORT);
  udp.write((const uint8_t*)msg.c_str(), msg.length());
  udp.endPacket();
  Serial.println("Sent discovery ping: " + msg);
}

void Minibot::stopAllMotors() {
  driveLeftMotor(0);
  driveRightMotor(0);
  driveDCMotor(0);
  driveServoMotor(0);
}

void Minibot::updateController() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) incomingPacket[len] = '\0';

    // Check if it's a game status packet (text format)
    String packetStr = String(incomingPacket);
    if (packetStr.startsWith(robotId)) {
      int sepIndex = packetStr.indexOf(':');
      if (sepIndex != -1) {
        gameStatus = stringToGameStatus(packetStr.substring(sepIndex + 1));
      }
    }

    // Decode controller data (binary format)
    char robotName[17];
    uint8_t axes[6];
    uint8_t buttons[2];

    memcpy(robotName, incomingPacket, 16);
    robotName[16] = '\0';
    memcpy(axes, incomingPacket + 16, 6);
    memcpy(buttons, incomingPacket + 22, 2);

    if (String(robotName) == robotId && gameStatus == Status::Teleop) {
      leftX = axes[0];
      leftY = axes[1];
      rightX = axes[2];
      rightY = axes[3];

      cross = buttons[0] & 0x01;
      circle = buttons[0] & 0x02;
      square = buttons[0] & 0x04;
      triangle = buttons[0] & 0x08;
    }
  }
}

int Minibot::getLeftX() { return leftX; }
int Minibot::getLeftY() { return leftY; }
int Minibot::getRightX() { return rightX; }
int Minibot::getRightY() { return rightY; }

bool Minibot::getCross() { return cross; }
bool Minibot::getCircle() { return circle; }
bool Minibot::getSquare() { return square; }
bool Minibot::getTriangle() { return triangle; }

Minibot::Status Minibot::getGameStatus() { return gameStatus; }

Minibot::Status Minibot::stringToGameStatus(String string)
{
    if (string == "standby")
    {
      return Status::Standby;
    }
    else if (string == "teleop")
    {
      return Status::Teleop;
    }
    return Status::Unknown;
}

bool Minibot::driveDCMotor(float value) {
  if (value < -1 || value > 1)
  {
    return false;
  }
  return ledcWrite(dcMotorPin, round((value*MOTOR_SPEED_MULTIPLYER)+dcMotorPwmOffset));
}

bool Minibot::driveLeftMotor(float value) {
  if (value < -1 || value > 1)
  {
    return false;
  }
  return ledcWrite(leftMotorPin, round((value*MOTOR_SPEED_MULTIPLYER)+leftMotorPwmOffset));
}

bool Minibot::driveRightMotor(float value) {
  if (value < -1 || value > 1)
  {
    return false;
  }
  return ledcWrite(rightMotorPin, round((value*MOTOR_SPEED_MULTIPLYER)+rightMotorPwmOffset));
}

bool Minibot::driveServoMotor(int angle) {
  if (angle < -50 || angle > 50) {
    return false;
  }
  float pulseWidthMs = 0.01 * angle + 1.5;
  int dutyCycle = (pulseWidthMs / 10.0) * 65535;
  ledcWrite(servoMotorPin, dutyCycle);
  return true;
}
