# Minibot Library Documentation

Welcome to the Minibot programming guide! This document will teach you everything you need to know to program your robot.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Setup Functions](#setup-functions)
3. [Getting Controller Input](#getting-controller-input)
4. [Controlling Motors](#controlling-motors)
5. [Game Status](#game-status)
6. [Complete Example Snippets](#complete-example-snippets)

---

## Getting Started

### What You Need to Know

Your robot code has two main parts:
- **`setup()`** - Runs once when the robot starts up
- **`loop()`** - Runs over and over again while the robot is on

Think of it like this:
- `setup()` is where you prepare everything (like setting up a game board)
- `loop()` is where the action happens (like playing the game over and over)

### Creating Your Robot

At the very top of your code (before `setup()`), you need to create your robot:

```cpp
Minibot bot("YOUR NAME HERE");
```

**What to put:**
- Replace `"YOUR NAME HERE"` with your actual name or robot name
- This name MUST match what's in the driver station computer
- Keep it short and simple (under 16 characters)

**Example:**
```cpp
Minibot bot("Alice");
```

---

## Setup Functions

### `bot.init()`

**What it does:** Initializes (starts up) your robot. This connects to WiFi, sets up the motors, and gets everything ready.

**When to use:** Call this once inside `setup()`, and nowhere else.

**How to use:**
```cpp
void setup() {
  bot.init();  // Always put this in setup!
}
```

**What happens:**
- Connects to the WiFi network
- Sets up all the motor pins
- Starts listening for controller commands
- Prints information to the Serial Monitor

---

## Getting Controller Input

These functions let you read what buttons and joysticks the driver is using. Call these inside `loop()` after calling `bot.updateController()`.

### `bot.updateController()`

**What it does:** Updates all the controller values from the driver station. You MUST call this at the beginning of your `loop()` to get the latest controller information.

**When to use:** At the very start of `loop()`, every single time.

**How to use:**
```cpp
void loop() {
  bot.updateController();  // Always first!

  // Now you can use all the controller values below
}
```

---

### Getting Joystick Values

The controller has two joysticks (left and right), and each joystick can move in two directions (X and Y).

#### `bot.getLeftX()`

**What it does:** Gets the left joystick's horizontal position (left/right).

**Returns:** A number from 0 to 255
- **0** = all the way left
- **125** = center (not pushed)
- **255** = all the way right

**Example:**
```cpp
int leftRight = bot.getLeftX();

if (leftRight > 150) {
  // Joystick is pushed to the right
}
```

---

#### `bot.getLeftY()`

**What it does:** Gets the left joystick's vertical position (up/down).

**Returns:** A number from 0 to 255
- **0** = all the way up
- **130** = center (not pushed)
- **255** = all the way down

**Example:**
```cpp
int upDown = bot.getLeftY();

if (upDown < 100) {
  // Joystick is pushed up
}
```

---

#### `bot.getRightX()`

**What it does:** Gets the right joystick's horizontal position (left/right).

**Returns:** A number from 0 to 255
- **0** = all the way left
- **127** = center (not pushed)
- **255** = all the way right

**Example:**
```cpp
int turning = bot.getRightX();

if (turning < 100) {
  // Right joystick is pushed left
}
```

---

#### `bot.getRightY()`

**What it does:** Gets the right joystick's vertical position (up/down).

**Returns:** A number from 0 to 255
- **0** = all the way up
- **130** = center (not pushed)
- **255** = all the way down

**Example:**
```cpp
int speed = bot.getRightY();

if (speed > 180) {
  // Right joystick is pushed down
}
```

---

### Getting Button Values

The controller has four main buttons: Cross (X), Circle (O), Square (□), and Triangle (△).

#### `bot.getCross()`

**What it does:** Checks if the Cross button (X) is pressed.

**Returns:**
- `true` if the button IS pressed
- `false` if the button is NOT pressed

**Example:**
```cpp
if (bot.getCross()) {
  // Cross button is being pressed!
  // Do something here
}
```

---

#### `bot.getCircle()`

**What it does:** Checks if the Circle button (O) is pressed.

**Returns:**
- `true` if the button IS pressed
- `false` if the button is NOT pressed

**Example:**
```cpp
if (bot.getCircle()) {
  // Circle button is being pressed!
}
```

---

#### `bot.getSquare()`

**What it does:** Checks if the Square button (□) is pressed.

**Returns:**
- `true` if the button IS pressed
- `false` if the button is NOT pressed

**Example:**
```cpp
if (bot.getSquare()) {
  // Square button is being pressed!
}
```

---

#### `bot.getTriangle()`

**What it does:** Checks if the Triangle button (△) is pressed.

**Returns:**
- `true` if the button IS pressed
- `false` if the button is NOT pressed

**Example:**
```cpp
if (bot.getTriangle()) {
  // Triangle button is being pressed!
}
```

---

## Controlling Motors

These functions let you control the motors on your robot. Motors make your robot move!

### `bot.drive(left, right)`

**What it does:** Controls both drive motors at the same time (the wheels that make your robot move).

**Parameters:**
- `left` - Speed for left motor (between -1.0 and 1.0)
- `right` - Speed for right motor (between -1.0 and 1.0)

**Speed values:**
- **-1.0** = full speed backward
- **0.0** = stopped
- **1.0** = full speed forward

**Returns:**
- `true` if successful
- `false` if the values are out of range

**Examples:**

Drive forward:
```cpp
bot.drive(1.0, 1.0);  // Both motors full speed forward
```

Drive backward:
```cpp
bot.drive(-1.0, -1.0);  // Both motors full speed backward
```

Turn right (spin in place):
```cpp
bot.drive(1.0, -1.0);  // Left forward, right backward
```

Turn left (spin in place):
```cpp
bot.drive(-1.0, 1.0);  // Left backward, right forward
```

Drive at half speed:
```cpp
bot.drive(0.5, 0.5);  // Both motors at 50% speed
```

Stop completely:
```cpp
bot.drive(0.0, 0.0);  // Both motors stopped
```

**Important:** You need to call this repeatedly in your `loop()` to keep the motors running!

---

### `bot.driveDCMotor(value)`

**What it does:** Controls an extra DC motor (not the drive wheels). You can use this for things like a launcher, conveyor belt, or intake mechanism.

**Parameters:**
- `value` - Motor speed (between -1.0 and 1.0)
  - **-1.0** = full speed backward
  - **0.0** = stopped
  - **1.0** = full speed forward

**Returns:**
- `true` if successful
- `false` if the value is out of range

**Examples:**

Run motor forward:
```cpp
bot.driveDCMotor(1.0);  // Full speed forward
```

Run motor backward:
```cpp
bot.driveDCMotor(-0.75);  // 75% speed backward
```

Stop motor:
```cpp
bot.driveDCMotor(0.0);  // Motor stopped
```

**Example use case - Intake mechanism:**
```cpp
if (bot.getCross()) {
  bot.driveDCMotor(1.0);  // Suck in when Cross is pressed
} else if (bot.getCircle()) {
  bot.driveDCMotor(-1.0);  // Spit out when Circle is pressed
} else {
  bot.driveDCMotor(0.0);  // Stop when nothing is pressed
}
```

---

### `bot.driveServoMotor(angle)`

**What it does:** Controls a servo motor. Servos move to specific positions (angles) instead of spinning continuously. Good for arms, claws, or tilting mechanisms.

**Parameters:**
- `angle` - Position to move to (between -50 and 50)
  - **-50** = all the way to one side
  - **0** = center position
  - **50** = all the way to the other side

**Returns:**
- `true` if successful
- `false` if the angle is out of range

**Examples:**

Move to center:
```cpp
bot.driveServoMotor(0);  // Servo at center
```

Move to one extreme:
```cpp
bot.driveServoMotor(-50);  // Servo all the way left
```

Move to other extreme:
```cpp
bot.driveServoMotor(50);  // Servo all the way right
```

Move to specific position:
```cpp
bot.driveServoMotor(25);  // Servo halfway between center and right
```

**Example use case - Claw control:**
```cpp
if (bot.getSquare()) {
  bot.driveServoMotor(50);  // Open claw
} else if (bot.getTriangle()) {
  bot.driveServoMotor(-50);  // Close claw
}
```

---

## Game Status

### `bot.getGameStatus()`

**What it does:** Tells you what mode the game is in.

**Returns:** A text string with the current status:
- `"standby"` - Robot is waiting, no driving allowed
- `"teleop"` - Teleop (tele-operated) mode, driver has control

**When to use:** You usually don't need this! The robot automatically ignores controller input during standby. But you can use it if you want to do something special in different modes.

**Example:**
```cpp
String status = bot.getGameStatus();

if (status == "teleop") {
  // Game is active
} else if (status == "standby") {
  // Waiting to start
}
```

---

## Complete Example Snippets

Here are some common patterns you'll use. Remember: these go in the `loop()` function!

### Tank Drive (Simple)

Each joystick controls one side of the robot:

```cpp
void loop() {
  bot.updateController();

  // Convert joystick values (0-255) to motor values (-1 to 1)
  float left = (bot.getLeftY() - 130.0) / 130.0;
  float right = (bot.getRightY() - 130.0) / 130.0;

  bot.drive(left, right);
}
```

### Arcade Drive (One Joystick)

One joystick controls forward/backward and turning:

```cpp
void loop() {
  bot.updateController();

  // Get joystick values
  float forward = (130.0 - bot.getLeftY()) / 130.0;  // Up is positive
  float turn = (bot.getLeftX() - 125.0) / 125.0;     // Right is positive

  // Calculate motor speeds
  float leftMotor = forward + turn;
  float rightMotor = forward - turn;

  bot.drive(leftMotor, rightMotor);
}
```

### Button-Controlled Mechanism

Use buttons to control an extra motor:

```cpp
void loop() {
  bot.updateController();

  // Your driving code here...

  // Button controls for DC motor
  if (bot.getCross()) {
    bot.driveDCMotor(1.0);   // Run forward
  } else if (bot.getCircle()) {
    bot.driveDCMotor(-1.0);  // Run backward
  } else {
    bot.driveDCMotor(0.0);   // Stop
  }
}
```

### Servo Position Control

Use buttons to move a servo to different positions:

```cpp
void loop() {
  bot.updateController();

  // Your driving code here...

  // Button controls for servo
  if (bot.getSquare()) {
    bot.driveServoMotor(-50);  // Position 1
  } else if (bot.getTriangle()) {
    bot.driveServoMotor(0);    // Position 2 (center)
  }
}
```

### Full Robot Template

Here's the complete structure of a robot program:

```cpp
#include "minibot.h"

// Create your robot (put your name here!)
Minibot bot("YourName");

void setup() {
  // Initialize the robot - runs once at startup
  bot.init();
}

void loop() {
  // Update controller values - ALWAYS FIRST!
  bot.updateController();

  // ===== YOUR CODE GOES BELOW =====

  // 1. Read joystick/button values
  // 2. Do calculations or logic
  // 3. Control motors

  // Example: Simple tank drive
  float left = (bot.getLeftY() - 130.0) / 130.0;
  float right = (bot.getRightY() - 130.0) / 130.0;
  bot.drive(left, right);

  // Example: Button-controlled mechanism
  if (bot.getCross()) {
    bot.driveDCMotor(1.0);
  } else {
    bot.driveDCMotor(0.0);
  }
}
```

---

## Tips and Tricks

### Converting Joystick Values to Motor Speeds

Joysticks give values 0-255, but motors need -1.0 to 1.0. Here's how to convert:

For Y-axis (up/down), where up should be positive:
```cpp
float motorSpeed = (130.0 - bot.getLeftY()) / 130.0;
```

For Y-axis (up/down), where down should be positive:
```cpp
float motorSpeed = (bot.getLeftY() - 130.0) / 130.0;
```

For X-axis (left/right), where right should be positive:
```cpp
float motorSpeed = (bot.getLeftX() - 125.0) / 125.0;
```

### Making Motors Less Sensitive

If your robot is too fast, multiply by a number less than 1:

```cpp
float speed = (bot.getLeftY() - 130.0) / 130.0;
speed = speed * 0.5;  // Now only 50% as fast
bot.drive(speed, speed);
```

### Dead Zone (Prevent Drift)

If your robot moves when the joystick is centered, add a dead zone:

```cpp
float speed = (bot.getLeftY() - 130.0) / 130.0;

// If joystick is close to center, set speed to zero
if (speed > -0.1 && speed < 0.1) {
  speed = 0.0;
}

bot.drive(speed, speed);
```

### Toggle With Buttons

Make a button turn something on/off (like a light switch):

```cpp
bool motorOn = false;  // Put this BEFORE setup()

void loop() {
  bot.updateController();

  if (bot.getCross()) {
    motorOn = !motorOn;  // Flip between true/false
    delay(200);          // Wait so it doesn't flip too fast
  }

  if (motorOn) {
    bot.driveDCMotor(1.0);
  } else {
    bot.driveDCMotor(0.0);
  }
}
```

---

## Quick Reference Chart

| Function | What It Does | Returns |
|----------|-------------|---------|
| `bot.init()` | Start up the robot | Nothing |
| `bot.updateController()` | Get latest controller data | Nothing |
| `bot.getLeftX()` | Left joystick left/right | 0-255 (125=center) |
| `bot.getLeftY()` | Left joystick up/down | 0-255 (130=center) |
| `bot.getRightX()` | Right joystick left/right | 0-255 (127=center) |
| `bot.getRightY()` | Right joystick up/down | 0-255 (130=center) |
| `bot.getCross()` | Cross button pressed? | true/false |
| `bot.getCircle()` | Circle button pressed? | true/false |
| `bot.getSquare()` | Square button pressed? | true/false |
| `bot.getTriangle()` | Triangle button pressed? | true/false |
| `bot.drive(left, right)` | Control drive motors | true if successful |
| `bot.driveDCMotor(speed)` | Control DC motor | true if successful |
| `bot.driveServoMotor(angle)` | Control servo motor | true if successful |
| `bot.getGameStatus()` | Get game mode | "standby" or "teleop" |

---

## Common Mistakes to Avoid

1. **Forgetting `bot.updateController()`** - Always call this first in `loop()`!

2. **Wrong value ranges** - Motors use -1.0 to 1.0, not 0 to 255

3. **Only calling motor functions once** - You need to keep calling them in `loop()` to keep motors running

4. **Case sensitivity** - `bot.getCross()` works, but `bot.getcross()` doesn't

5. **Not matching robot name** - The name in your code must match the driver station

---

Good luck programming your robot! 🤖
