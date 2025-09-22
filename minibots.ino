#include <WiFi.h>
#include <WiFiUdp.h>

// Wi-Fi credentials
const char* ssid = "WATCHTOWER";
const char* password = "lancerrobotics";
const char* robot_id = "minibot_ex";

// UDP setup
WiFiUDP udp;
const unsigned int localPort = 2367;
char incomingPacket[255];
String gameStatus = "standby";

// Motor pins
#define LEFT_MOTOR_FORWARD  5
#define LEFT_MOTOR_BACKWARD 18
#define RIGHT_MOTOR_FORWARD 19
#define RIGHT_MOTOR_BACKWARD 21

void setup() {
  Serial.begin(115200);

  // Motor setup
  pinMode(LEFT_MOTOR_FORWARD, OUTPUT);
  pinMode(LEFT_MOTOR_BACKWARD, OUTPUT);
  pinMode(RIGHT_MOTOR_FORWARD, OUTPUT);
  pinMode(RIGHT_MOTOR_BACKWARD, OUTPUT);

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

void moveForward() {
  digitalWrite(LEFT_MOTOR_FORWARD, HIGH);
  digitalWrite(LEFT_MOTOR_BACKWARD, LOW);
  digitalWrite(RIGHT_MOTOR_FORWARD, HIGH);
  digitalWrite(RIGHT_MOTOR_BACKWARD, LOW);
}

void moveBackward() {
  digitalWrite(LEFT_MOTOR_FORWARD, LOW);
  digitalWrite(LEFT_MOTOR_BACKWARD, HIGH);
  digitalWrite(RIGHT_MOTOR_FORWARD, LOW);
  digitalWrite(RIGHT_MOTOR_BACKWARD, HIGH);
}

void spinRight() {
  digitalWrite(LEFT_MOTOR_FORWARD, HIGH);
  digitalWrite(LEFT_MOTOR_BACKWARD, LOW);
  digitalWrite(RIGHT_MOTOR_FORWARD, LOW);
  digitalWrite(RIGHT_MOTOR_BACKWARD, HIGH);
}

void stopMotors() {
  digitalWrite(LEFT_MOTOR_FORWARD, LOW);
  digitalWrite(LEFT_MOTOR_BACKWARD, LOW);
  digitalWrite(RIGHT_MOTOR_FORWARD, LOW);
  digitalWrite(RIGHT_MOTOR_BACKWARD, LOW);
}

void loop() {
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
        Serial.println("Game status: " + gameStatus);
        return; // Skip decoding controller data
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


    if (String(robotName) == robot_id) {
      Serial.println("Controller data received for this robot:");
      for (int i = 0; i < 6; i++) {
        Serial.print("Axis ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(axes[i]);
      }
      Serial.print("Buttons: ");
      Serial.print(buttons[0], BIN);
      Serial.print(" ");
      Serial.println(buttons[1], BIN);
    }
  }
  delay(100);
}
