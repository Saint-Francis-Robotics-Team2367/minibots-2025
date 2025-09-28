#include <WiFi.h>
#include <WiFiUdp.h>
#include <algorithm>

// Controller Values
int leftX = 125; // Default value
int leftY = 130; // Default value
int rightX = 127; // Default value
int rightY = 130; // Default value
bool cross = 0; // Default value of false
bool circle = 0; // Default value of false
bool square = 0; // Default value of false
bool triangle = 0; // Default value of false

// Wi-Fi credentials
const char* ssid = "WATCHTOWER";
const char* password = "lancerrobotics";
const char* robot_id = "minibot_ex"; // replace "ROBOT_NAME" with your team name, make sure your team name is between double quotes

// UDP setup
WiFiUDP udp;
const unsigned int localPort = 2367;
char incomingPacket[255];
String gameStatus = "standby";

// Motor Pins
#define leftPin 16
#define rightPin 17

void setup() {
  Serial.begin(115200);

  pinMode(leftPin, OUTPUT);
  pinMode(rightPin, OUTPUT);

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


// Give value between -1 and 1
bool drive(int pin, int value) {
  if (value < -1 || value > 1) {
    return false;
  }
  int delayAmt = 0.5*value + 1.5;
  digitalWrite(pin, HIGH);
  delay(delayAmt);
  digitalWrite(pin, LOW);
  delay(10-delayAmt);
  return true;
}

void updateControllerVals() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) incomingPacket[len] = '\0';

    // Check if it's a game status packet (text format)
    String packetStr = String(incomingPacket);
    if (packetStr.startsWith(robot_id)) {
      int sepIndex = packetStr.indexOf(':');
      if (sepIndex != -1) {
        gameStatus = packetStr.substring(sepIndex + 1);
        //Serial.println("Game status: " + gameStatus);
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

    // Axis 0: Left Joystick Horizontal (253 Right)
    // Axis 1: Left Joystick Vertical (253 Down)
    // Axis 2: Right Joystick Horizontal (253 Right)
    // Axis 3: Right Joystick Vertical (253 Down)
    // Axis 4: Left Trigger (253 Pressed)
    // Axis 5: Right Trigger (253 Pressed)
    
    if (String(robotName) == robot_id && gameStatus == "teleop") {
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

void loop() {
  updateControllerVals();
  Serial.println(gameStatus);
  Serial.println(leftX);
  Serial.println(leftY);
  Serial.println(rightX);
  Serial.println(rightY);

  Serial.println(cross);
  Serial.println(circle);
  Serial.println(square);
  Serial.println(triangle);
  Serial.println();
}