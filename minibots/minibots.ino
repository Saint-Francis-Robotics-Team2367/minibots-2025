#include <driver/ledc.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// Wi-Fi credentials
float left = 0;
float right = 0;
int leftX = 0;
int leftY = 0;
int rightX = 0;
int rightY = 0;
const int freq = 50;
const int resolution = 10;
const char* ssid = "ROBOWIFINET";
const char* password = "robo8711$$W";
const char* robot_id = "SERV";

// UDP setup
WiFiUDP udp;
const unsigned int localPort = 2367;
char incomingPacket[255];
String gameStatus = "standby";

// Motor pins
#define leftMotorPin  18
#define rightMotorPin 19

void setup() {
  Serial.begin(115200);

  // Motor setup
  ledcAttach(leftMotorPin, freq, resolution);
  ledcAttach(rightMotorPin, freq, resolution);

  // Wi-Fi connection
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  // Start UDP
  udp.begin(localPort);
  Serial.println("Listening on UDP port " + String(localPort));
}

bool driveRightMotor(float value) {
  float clampedVal = std::clamp(value*20, -20.0f, 20.0f);
  return ledcWrite(rightMotorPin, round(clampedVal + 75));
}

bool driveLeftMotor(float value) {
  float clampedVal = std::clamp(value*20, -20.0f, 20.0f);
  return ledcWrite(leftMotorPin, round(clampedVal + 75));
}

void stopAllMotors() {
  driveLeftMotor(0);
  driveRightMotor(0);
}

int getLeftX() { return leftX; }
int getLeftY() { return leftY; }
int getRightX() { return rightX; }
int getRightY() { return rightY; }

void loop() {
  int packetSize = udp.parsePacket();
if (packetSize) {
  int len = udp.read(incomingPacket, 255);
  if (len > 0) incomingPacket[len] = '\0';

  // Check if it's a binary packet
  if (packetSize == 24) {
    char robotName[17];
    uint8_t axes[6];
    uint8_t buttons[2];

    memcpy(robotName, incomingPacket, 16);
    robotName[16] = '\0';
    memcpy(axes, incomingPacket + 16, 6);
    memcpy(buttons, incomingPacket + 22, 2);

    if (String(robotName) == robot_id) {
      leftX = axes[0];
      leftY = axes[1];
      rightX = axes[2];
      rightY = axes[3];

      Serial.print("Left Y: ");
      Serial.println(leftY);
      Serial.print("Right Y: ");
      Serial.println(rightY);
    }
  } else {
    // Treat as text packet
    String packetStr = String(incomingPacket);
    if (packetStr.startsWith(robot_id)) {
      int sepIndex = packetStr.indexOf(':');
      if (sepIndex != -1) {
        gameStatus = packetStr.substring(sepIndex + 1);
        Serial.println("Game status: " + gameStatus);
      }
    } else {
      Serial.println("Unrecognized packet: " + packetStr);
    }
  }
}


//  Serial.println("Game Status: " + gameStatus);
//  Serial.println("Left Y: " + leftY);
//  Serial.println("Right Y: " + rightY);
  
  if (gameStatus != "standby") {
      left = (leftY < 130 && leftY > 125) ? 0.0 : -1*(leftY) / 128.0 + 1;
      right = (rightY < 130 && rightY > 125) ? 0.0 : -1*(rightY) / 128.0 + 1;
      Serial.print("Left Speed: ");
      Serial.println(left);
      Serial.print("Right Speed: ");
      Serial.println(right);
      driveLeftMotor(left);
      driveRightMotor(right);
  }
  else {
      stopAllMotors();
  }
}