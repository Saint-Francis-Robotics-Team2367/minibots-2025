# Minibot Library Documentation

Welcome to the Minibot programming guide! This document will teach you everything you need to know to program your robot.

## Table of Contents
1. [Getting Started](#getting-started)
2. [How Your Robot Connects](#how-your-robot-connects)
3. [Setup Functions](#setup-functions)
4. [Getting Controller Input](#getting-controller-input)
5. [Controlling Motors](#controlling-motors)
6. [Game Status](#game-status)
7. [Emergency Stop](#emergency-stop)
8. [Complete Example Snippets](#complete-example-snippets)

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

## How Your Robot Connects

Your robot uses a smart connection system to find and connect to the driver station. Here's what happens automatically behind the scenes:

### Discovery Mode

When your robot first starts up, it enters **discovery mode**:
- It connects to the WiFi network "WATCHTOWER"
- Every 2 seconds, it sends out a "discovery ping" broadcast message
- This message says: "Hey! I'm here! My name is [your robot name]"
- The driver station listens for these pings and responds when it finds your robot

**What you see:**
- The Serial Monitor will show "Sent discovery ping: DISCOVER:YourName:192.168.x.x"
- Your robot is announcing itself and waiting to be found

### Port Assignment

Once the driver station hears your robot's discovery ping:
- It assigns your robot a unique port number (like a private communication channel)
- It sends back a "PORT" message with your assigned port
- Your robot switches from the discovery port (12345) to this assigned port
- Now you have a dedicated connection!

**What you see:**
- The Serial Monitor will show "Assigned port 12346 - connected!"
- Your robot is now fully connected and ready to receive commands

### Connection Timeout

Your robot is smart about staying connected:
- If it doesn't receive any commands for **5 seconds**, it assumes the connection was lost
- It automatically goes back to discovery mode to reconnect
- All motors stop for safety when disconnected

**Why this matters:**
- If the driver station crashes or loses connection, your robot won't run wild
- It will safely stop and wait to reconnect
- You'll see "Connection timeout - reverting to discovery mode" in the Serial Monitor

### What This Means For You

**Good news:** You don't have to do anything! This all happens automatically.

Just create your robot with its name, and the library handles:
- Finding the driver station
- Getting assigned a port
- Reconnecting if something goes wrong
- Stopping motors safely when disconnected

---

## Setup Functions

### Automatic Initialization

**Good news:** Your robot initializes automatically when it's created!

When you create your Minibot with `Minibot bot("YourName");`, it automatically:
- Connects to the WiFi network "WATCHTOWER"
- Sets up all the motor pins with PWM (Pulse Width Modulation)
- Starts the UDP discovery system
- Stops all motors (safe starting position)
- Prints connection information to the Serial Monitor

**What you'll see in Serial Monitor:**
```
Connecting to WiFi...
Connected! IP: 192.168.1.100
Listening on discovery port 12345
Sent discovery ping: DISCOVER:YourName:192.168.1.100
```

**What this means:** You don't need to call any special setup function! Just create your robot, and you're ready to go.

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

## Emergency Stop

The robot has a built-in emergency stop (ESTOP) feature for safety. This is controlled by the driver station, not your code.

### What is Emergency Stop?

**Emergency stop** is a safety feature that immediately stops all motors on your robot. When activated:
- **All motors stop instantly** (drive motors, DC motor, and servo motor)
- **Motor commands are ignored** - even if your code tries to move motors, they won't respond
- **The robot stays stopped** until the emergency stop is released

### When Does It Activate?

The driver station operator can activate emergency stop:
- By pressing the emergency stop button on the driver station
- When something goes wrong and they need to stop the robot immediately
- For safety during setup or troubleshooting

### What You'll See

**When emergency stop activates:**
- Serial Monitor shows: "EMERGENCY STOP ACTIVATED"
- All motors stop immediately
- Your robot is frozen (safe state)

**When emergency stop is released:**
- Serial Monitor shows: "Emergency stop released"
- Robot returns to normal operation
- Your code can control motors again

### Do You Need to Do Anything?

**Nope!** Emergency stop is handled automatically by the library.

- You don't need to write any code for emergency stop
- You don't need to check if emergency stop is active
- Your motor commands will automatically work or not work based on the emergency stop state

**Why this matters:**
- Safety first! If something goes wrong, the driver station can immediately stop your robot
- You can focus on writing your robot code without worrying about emergency stop logic
- The system handles it all in the background

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
// This automatically connects to WiFi and sets everything up
Minibot bot("YourName");

void setup() {
  // Nothing needed here! The robot initializes automatically when created
  // You can add your own setup code here if needed
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
