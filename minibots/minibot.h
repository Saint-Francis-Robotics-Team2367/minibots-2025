#ifndef MINIBOT_H
#define MINIBOT_H

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiUdp.h>

// PWM Channel Definitions
const int LEFT_PWM_CHANNEL = 0;
const int RIGHT_PWM_CHANNEL = 1;
const int DC_PWM_CHANNEL = 2;
const int SERVO_PWM_CHANNEL = 3;

// WiFi Configuration (define these in your main file or config)
#ifndef WIFI_SSID
#define WIFI_SSID "your_wifi_ssid"
#endif

#ifndef WIFI_PASSWORD
#define WIFI_PASSWORD "your_wifi_password"
#endif

#ifndef UDP_PORT
#define UDP_PORT 8888
#endif

class Minibot {
private:
    const char* robotId;
    int leftPin;
    int rightPin;
    int dcMotorPin;
    int servoMotorPin;
    
    int leftX;
    int leftY;
    int rightX;
    int rightY;
    
    bool cross;
    bool circle;
    bool square;
    bool triangle;
    
    String gameStatus;
    
    WiFiUDP udp;
    char incomingPacket[256];

public:
    // Constructor
    Minibot(const char* robotId, 
            int leftMotorPin, int rightMotorPin,
            int dcMotorPin, int servoMotorPin);
    
    // Update controller state from UDP packets
    void updateController();
    
    // Getter methods for joystick axes
    int getLeftX();
    int getLeftY();
    int getRightX();
    int getRightY();
    
    // Getter methods for buttons
    bool getCross();
    bool getCircle();
    bool getSquare();
    bool getTriangle();
    
    // Get game status
    String getGameStatus();
    
    // Motor control methods
    bool driveDCMotor(float value);      // value: -1.0 to 1.0
    bool driveLeft(float value);         // value: -1.0 to 1.0
    bool driveRight(float value);        // value: -1.0 to 1.0
    bool driveServoMotor(int angle);     // angle: -50 to 50 degrees
};

#endif // MINIBOT_H