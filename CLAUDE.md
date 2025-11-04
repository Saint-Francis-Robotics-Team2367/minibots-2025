# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Arduino-based robotics competition codebase for minibots. The system consists of:
- **Arduino firmware** (ESP32-based minibots) that receive controller input via WiFi/UDP
- **Python driver station** that broadcasts controller data to robots over the network

## Architecture

### Minibot Class (`minibots/minibot.h`, `minibots/minibot.cpp`)
Core abstraction for robot control:
- **Network**: Connects to WiFi network "WATCHTOWER", listens for UDP packets on port 2367
- **Controller Input**: Receives binary UDP packets containing robot name (16 bytes), axis values (6 bytes), and button states (2 bytes)
- **Game Modes**: Responds to game status messages ("standby", "teleop") - only processes controller input during "teleop"
- **Motor Control**:
  - `drive(float left, float right)`: Controls left/right drive motors with values -1 to 1
  - `driveDCMotor(float value)`: Controls DC motor with value -1 to 1
  - `driveServoMotor(int angle)`: Controls servo with angle -50 to 50
  - All motor functions use PWM via digitalWrite with calculated delay timing

### Driver Station (`driverStation.py`)
Python application that:
- Uses pygame for controller input and tkinter for GUI
- Broadcasts controller data at 20Hz (50ms interval)
- Broadcasts game status updates every 1 second
- Supports multiple robots with individual controller assignments
- Game modes: "standby" (no input processed by robots) and "teleop" (full control)

### Main Sketch (`minibots/minibots.ino`)
Entry point for robot code:
- Creates `Minibot` object with robot name (must match driver station config)
- Default motor pins: left=16, right=17, dcMotor=18, servoMotor=19
- Calls `bot.init()` in setup() to initialize WiFi and motors
- Calls `bot.updateController()` in loop() to refresh controller values
- Students write robot control logic in loop() using getter methods

## Development Workflow

### Uploading to Arduino
Use Arduino IDE or arduino-cli to upload the sketch in the `minibots/` directory to an ESP32 board.

### Running Driver Station
```bash
python driverStation.py
```
Requires pygame and tkinter. Configure robot names in the `robots` list at the top of the file.

## Important Implementation Details

### Controller Value Ranges
- Joystick axes: 0-255 (center values: leftX≈125, leftY≈130, rightX≈127, rightY≈130)
- Buttons: boolean values (cross, circle, square, triangle)
- Convert joystick values to motor control by mapping to -1 to 1 range

### Network Protocol
- Robot identification via 16-character null-padded string
- Binary packet structure: `[16 bytes: name][6 bytes: axes][2 bytes: buttons]`
- Game status packets: text format `"robotName:status"`
- Robot only processes controller input when gameStatus == "teleop"

### Motor Control Timing
Motors use software PWM with 10ms cycle period:
- Drive motors: delay = 0.5 * value + 1.5 (value range -1 to 1)
- Servo motor: delay = 0.01 * angle + 1.5 (angle range -50 to 50)
