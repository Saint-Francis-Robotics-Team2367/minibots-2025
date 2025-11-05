import socket
import pygame
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import struct

# === Configuration ===
BROADCAST_PORT = 2367
robots = []
shutdown_flag = False
comm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
comm_socket.bind(('', BROADCAST_PORT))
comm_socket.setblocking(False)

game_status = "standby"
timer_running = False
timer_seconds = 180
default_duration = 180

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

status_var = tk.StringVar(value="Status: Standby")
timer_var = tk.StringVar(value="Timer: 03:00")
duration_var = tk.StringVar(value="180")
infinity_mode = tk.BooleanVar(value=False)

def set_status(new_status):
    global game_status, timer_running
    if timer_running and game_status == "teleop" and new_status != "standby":
        print("Cannot change status during active teleop.")
        return
    if new_status == "standby":
        timer_running = False
        teleop_button.config(text="Start Teleop")
    game_status = new_status
    status_var.set(f"Status: {new_status.capitalize()}")

def encode_controller_data(controller):
    axes = [int((controller.get_axis(i) * 127) + 127) & 0xFF for i in range(6)]
    buttons = sum((controller.get_button(i) << i) for i in range(4))
    return struct.pack('6B2B', *axes, buttons & 0xFF, (buttons >> 8) & 0xFF)

def discover_robots():
    while not shutdown_flag:
        try:
            comm_socket.sendto(b"ping", ('255.255.255.255', BROADCAST_PORT))
            data, addr = comm_socket.recvfrom(1024)
            if data.startswith(b"pong:"):
                name = data[5:].decode().strip()
                existing = next((r for r in robots if r["name"] == name), None)
                if not existing:
                    robots.append({"name": name, "controller": None, "addr": addr})
                    print(f"Discovered new robot: {name} at {addr}")
                    robot1_dropdown['values'] = [r["name"] for r in robots]
                    robot2_dropdown['values'] = [r["name"] for r in robots]
                else:
                    existing["addr"] = addr
        except BlockingIOError:
            pass
        except OSError:
            break
        time.sleep(0.05)

def send_controller_data():
    while not shutdown_flag:
        try:
            pygame.event.pump()
            for robot in robots:
                controller = robot["controller"]
                if controller and "addr" in robot:
                    data = encode_controller_data(controller)
                    comm_socket.sendto(data, robot["addr"])
        except OSError:
            break
        time.sleep(0.05)

def broadcast_game_status():
    while not shutdown_flag:
        try:
            current_status = "teleop" if timer_running and (timer_seconds > 0 or timer_seconds == -1) else "standby"
            for robot in robots:
                if "addr" in robot:
                    packet = f"{robot['name']}:{current_status}".encode()
                    comm_socket.sendto(packet, robot["addr"])
        except OSError:
            break
        time.sleep(1)

def connect_robot(robot_name, controller_name):
    robot = next((r for r in robots if r["name"] == robot_name), None)
    controller = next((c for c in active_controllers if c["name"] == controller_name), None)
    if robot and controller:
        robot["controller"] = controller["obj"]
        print(f"Connected {robot_name} to {controller_name}")
    else:
        print("Connection failed")

def refresh_controllers():
    global active_controllers
    pygame.joystick.quit()
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
    controller1_dropdown['values'] = [c["name"] for c in active_controllers]
    controller2_dropdown['values'] = [c["name"] for c in active_controllers]
    print("Controllers refreshed.")

def run_timer():
    global timer_running, timer_seconds
    while timer_running and (timer_seconds > 0 or timer_seconds == -1):
        if timer_seconds != -1:
            mins, secs = divmod(timer_seconds, 60)
            timer_var.set(f"Timer: {mins:02}:{secs:02}")
            timer_seconds -= 1
        else:
            timer_var.set("Timer: ∞")
        time.sleep(1)
    if timer_seconds == 0:
        set_status("standby")
        timer_var.set("Timer: 00:00")

def start_teleop():
    global timer_running, timer_seconds, default_duration
    if timer_seconds == 0:
        print("Timer expired. Reset before starting.")
        return

    if not timer_running:
        if infinity_mode.get():
            timer_seconds = -1
            timer_var.set("Timer: ∞")
        else:
            try:
                default_duration = int(duration_var.get())
            except ValueError:
                default_duration = 180
            timer_seconds = default_duration
            timer_var.set(f"Timer: {default_duration // 60:02}:{default_duration % 60:02}")
        timer_running = True
        set_status("teleop")
        teleop_button.config(text="Pause Teleop")

        for robot in robots:
            if "addr" in robot:
                packet = f"{robot['name']}:teleop".encode()
                comm_socket.sendto(packet, robot["addr"])

        Thread(target=run_timer, daemon=True).start()
    else:
        timer_running = False
        teleop_button.config(text="Start Teleop")

def stop_timer():
    global timer_running
    timer_running = False
    set_status("standby")

def reset_timer():
    global timer_running, timer_seconds, default_duration
    timer_running = False
    if infinity_mode.get():
        timer_seconds = -1
        timer_var.set("Timer: ∞")
    else:
        try:
            default_duration = int(duration_var.get())
        except ValueError:
            default_duration = 180
        timer_seconds = default_duration
        timer_var.set(f"Timer: {default_duration // 60:02}:{default_duration % 60:02}")
    teleop_button.config(text="Start Teleop")

def on_close():
    global shutdown_flag
    shutdown_flag = True
    time.sleep(0.1)
    comm_socket.close()
    root.destroy()

# === GUI Layout ===
tk.Label(root, text="Driver Station Control", font=("Arial", 16)).pack(pady=10)
tk.Label(root, textvariable=status_var, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Standby", width=20, command=lambda: set_status("standby")).pack(pady=2)

teleop_button = tk.Button(root, text="Start Teleop", width=20, command=start_teleop)
teleop_button.pack(pady=2)

tk.Label(root, textvariable=timer_var, font=("Arial", 12)).pack(pady=5)
tk.Label(root, text="Set Timer Duration (seconds):").pack()
tk.Entry(root, textvariable=duration_var).pack()
tk.Checkbutton(root, text="Infinity Mode", variable=infinity_mode).pack(pady=2)

tk.Button(root, text="Stop Timer", width=20, command=stop_timer).pack(pady=2)
tk.Button(root, text="Reset Timer", width=20, command=reset_timer).pack(pady=2)
tk.Button(root, text="Refresh Controllers", width=20, command=refresh_controllers).pack(pady=5)

# Robot 1
frame1 = tk.LabelFrame(root, text="Robot 1", padx=10, pady=10)
frame1.pack(padx=10, pady=5)
robot1_var = tk.StringVar()
robot1_dropdown = ttk.Combobox(frame1, textvariable=robot1_var, values=[r["name"] for r in robots], state="readonly")
robot1_dropdown.pack()
controller1_var = tk.StringVar()
controller1_dropdown = ttk.Combobox(frame1, textvariable=controller1_var, values=[c["name"] for c in active_controllers], state="readonly")
controller1_dropdown.pack()
tk.Button(frame1, text="Connect", command=lambda: connect_robot(robot1_var.get(), controller1_var.get())).pack()

# Robot 2
frame2 = tk.LabelFrame(root, text="Robot 2", padx=10, pady=10)
frame2.pack(padx=10, pady=5)
robot2_var = tk.StringVar()
robot2_dropdown = ttk.Combobox(frame2, textvariable=robot2_var, values=[r["name"] for r in robots], state="readonly")
robot2_dropdown.pack()
controller2_var = tk.StringVar()
controller2_dropdown = ttk.Combobox(frame2, textvariable=controller2_var, values=[c["name"] for c in active_controllers], state="readonly")
controller2_dropdown.pack()
tk.Button(frame2, text="Connect", command=lambda: connect_robot(robot2_var.get(), controller2_var.get())).pack()

# === Threads ===
Thread(target=discover_robots, daemon=True).start()
Thread(target=send_controller_data, daemon=True).start()
Thread(target=broadcast_game_status, daemon=True).start()

# === Run GUI ===
root.mainloop()
comm_socket.close()

