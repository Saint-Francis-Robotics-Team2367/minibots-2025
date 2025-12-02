import socket
import pygame
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import struct

# === Configuration ===
BROADCAST_PORT = 2367
robots = [
    {"name": "Crackens", "controller": None},
    {"name": "Metal Monkeys", "controller": None},
    {"name": "Low Power Mode", "controller": None},
    {"name": "Nut and Bolts", "controller": None},
    {"name": "Ironclad", "controller": None},
    {"name": "|noitalfni|", "controller": None},
    {"name": "Da Botz", "controller": None},
    {"name": "SuperWhy", "controller": None},
    {"name": "Bot Warriors", "controller": None},
    {"name": "SERV", "controller": None},
    {"name": "Trash Pickup", "controller": None},
    {"name": "Manipulators", "controller": None}
]

online_robots = [None, None]

# === UDP Setup ===
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# === Game State ===
game_status = "standby"

# === Pygame Controller Setup ===
pygame.init()
pygame.joystick.init()
active_controllers = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    active_controllers.append({
        "id": i,
        "name": f"{i}: {joystick.get_name()}",
        "obj": joystick
    })

# === Tkinter GUI ===
root = tk.Tk()
root.title("Driver Station")
status_var = tk.StringVar()
status_var.set("Status: Standby")

def set_status(new_status):
    global game_status
    game_status = new_status
    status_var.set(f"Status: {new_status.capitalize()}")

def encode_controller_data(controller, robot_name):
    name_bytes = robot_name.encode()[:16].ljust(16, b'\x00')
    axes = []
    for i in range(6):
        try:
            val = int((controller.get_axis(i) * 127) + 127) & 0xFF
        except Exception:
            val = 127  # neutral value
        axes.append(val)
    buttons = sum((controller.get_button(i) << i) for i in range(2))
    return struct.pack('16s6B2B', name_bytes, *axes, buttons & 0xFF, (buttons >> 8) & 0xFF)


def send_controller_data():
    while True:
        pygame.event.pump()
        for robot in online_robots:
            if robot == None: continue
            controller = robot["controller"]
            if controller:
                data = encode_controller_data(controller, robot["name"])
                broadcast_socket.sendto(data, ("<broadcast>", BROADCAST_PORT))
        time.sleep(0.05)

def broadcast_game_status():
    while True:
        for robot in online_robots:
            if robot == None: continue
            packet = f"{robot['name']}:{game_status}".encode()
            broadcast_socket.sendto(packet, ("<broadcast>", BROADCAST_PORT))
        time.sleep(1)

def connect_robot(robot_name, controller_name, robot_index):
    robot = next((r for r in robots if r["name"] == robot_name), None)
    controller = next((c for c in active_controllers if c["name"] == controller_name), None)
    if robot and controller:
        robot["controller"] = controller["obj"]
        online_robots[robot_index] = robot
        print(f"Connected {robot_name} to {controller_name}")
    else:
        print("Connection failed")

# === GUI Layout ===
tk.Label(root, text="Driver Station Control", font=("Arial", 16)).pack(pady=10)
tk.Label(root, textvariable=status_var, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Standby", width=20, command=lambda: set_status("standby")).pack(pady=2)
tk.Button(root, text="Teleop", width=20, command=lambda: set_status("teleop")).pack(pady=2)

# Robot 1
frame1 = tk.LabelFrame(root, text="Robot 1", padx=10, pady=10)
frame1.pack(padx=10, pady=5)
robot1_var = tk.StringVar()
robot1_dropdown = ttk.Combobox(frame1, textvariable=robot1_var, values=[r["name"] for r in robots], state="readonly")
robot1_dropdown.pack()
controller1_var = tk.StringVar()
controller1_dropdown = ttk.Combobox(frame1, textvariable=controller1_var, values=[c["name"] for c in active_controllers], state="readonly")
controller1_dropdown.pack()
tk.Button(frame1, text="Connect", command=lambda: connect_robot(robot1_var.get(), controller1_var.get(),0)).pack()

# Robot 2
frame2 = tk.LabelFrame(root, text="Robot 2", padx=10, pady=10)
frame2.pack(padx=10, pady=5)
robot2_var = tk.StringVar()
robot2_dropdown = ttk.Combobox(frame2, textvariable=robot2_var, values=[r["name"] for r in robots], state="readonly")
robot2_dropdown.pack()
controller2_var = tk.StringVar()
controller2_dropdown = ttk.Combobox(frame2, textvariable=controller2_var, values=[c["name"] for c in active_controllers], state="readonly")
controller2_dropdown.pack()
tk.Button(frame2, text="Connect", command=lambda: connect_robot(robot2_var.get(), controller2_var.get(),1)).pack()

# === Threads ===
Thread(target=send_controller_data, daemon=True).start()
Thread(target=broadcast_game_status, daemon=True).start()

# === Run GUI ===
root.mainloop()
broadcast_socket.close()

