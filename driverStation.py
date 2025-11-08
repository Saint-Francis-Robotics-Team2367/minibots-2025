import socket
import pygame
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import struct
import signal
import sys

try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False
    print("Warning: netifaces module not found. Install with: pip install netifaces")

# === Configuration ===
BROADCAST_PORT = 2367
robots = []

# Get the broadcast address for the active network interface
def get_broadcast_address():
    """Get the broadcast address of the network interface"""
    if NETIFACES_AVAILABLE:
        try:
            # Get all network interfaces
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                # Check if interface has IPv4
                if netifaces.AF_INET in addrs:
                    for addr_info in addrs[netifaces.AF_INET]:
                        ip = addr_info.get('addr')
                        broadcast = addr_info.get('broadcast')
                        # Skip loopback
                        if ip and broadcast and not ip.startswith('127.'):
                            print(f"Using network interface {interface}: IP={ip}, Broadcast={broadcast}")
                            return broadcast
        except Exception as e:
            print(f"Error getting broadcast address: {e}")
    
    # Try to get local IP and calculate broadcast
    try:
        # Create a socket to find our IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Local IP: {local_ip}")
        # For common /24 network, calculate broadcast
        ip_parts = local_ip.split('.')
        broadcast = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
        print(f"Calculated broadcast address: {broadcast}")
        return broadcast
    except Exception as e:
        print(f"Could not determine local IP: {e}")
    
    # Fallback to 255.255.255.255
    print("Using fallback broadcast address: 255.255.255.255")
    return '255.255.255.255'

broadcast_addr = get_broadcast_address()

comm_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comm_socket.bind(('', BROADCAST_PORT))
comm_socket.setblocking(False)

running = True

print(f"Driver Station started on port {BROADCAST_PORT}")
print(f"Broadcasting to {broadcast_addr}:{BROADCAST_PORT}")

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

def encode_controller_data(controller):
    axes = [int((controller.get_axis(i) * 127) + 127) & 0xFF for i in range(6)]
    
    # Read up to 16 buttons (adjust as needed)
    buttons = sum((controller.get_button(i) << i) for i in range(4))
    
    return struct.pack('6B2B', *axes, buttons & 0xFF, (buttons >> 8) & 0xFF)

def discover_robots():
    ping_count = 0
    last_ping_time = 0
    while running:
        current_time = time.time()
        
        # Send ping every 0.5 seconds (not every loop iteration)
        if current_time - last_ping_time >= 0.5:
            try:
                comm_socket.sendto(b"ping", (broadcast_addr, BROADCAST_PORT))
                ping_count += 1
                last_ping_time = current_time
                if ping_count % 10 == 0:  # Print every 5 seconds (10 * 0.5s)
                    print(f"Sent {ping_count} pings, discovered {len(robots)} robot(s)")
            except Exception as e:
                if running:
                    print(f"Error sending ping: {e}")
                break
        
        # Check for responses multiple times per ping cycle
        try:
            data, addr = comm_socket.recvfrom(1024)
            if data.startswith(b"pong:"):
                name = data[5:].decode().strip()
                print(f"Received pong from {name} at {addr}")

                # Check if already known
                existing = next((r for r in robots if r["name"] == name), None)
                if not existing:
                    robots.append({"name": name, "controller": None, "addr": addr})
                    print(f"✓ Discovered new robot: {name} at {addr}")

                    robot1_dropdown['values'] = [r["name"] for r in robots]
                    robot2_dropdown['values'] = [r["name"] for r in robots]
                else:
                    existing["addr"] = addr
        except BlockingIOError:
            pass
        except Exception as e:
            if running:
                print(f"Error in discovery: {e}")
            break
        
        time.sleep(0.02)  # Check for responses more frequently

def send_controller_data():
    while running:
        pygame.event.pump()
        for robot in robots:
            controller = robot["controller"]
            if controller and "addr" in robot:
                try:
                    data = encode_controller_data(controller)
                    comm_socket.sendto(data, robot["addr"])
                except Exception as e:
                    if running:
                        print(f"Error sending controller data: {e}")
                    break
        time.sleep(0.05)


def broadcast_game_status():
    while running:
        for robot in robots:
            if "addr" in robot:
                try:
                    packet = f"{robot['name']}:{game_status}".encode()
                    comm_socket.sendto(packet, robot["addr"])
                except Exception as e:
                    if running:
                        print(f"Error broadcasting status: {e}")
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

    # Update dropdowns
    controller1_dropdown['values'] = [c["name"] for c in active_controllers]
    controller2_dropdown['values'] = [c["name"] for c in active_controllers]
    print("Controllers refreshed.")

# === GUI Layout ===
tk.Label(root, text="Driver Station Control", font=("Arial", 16)).pack(pady=10)
tk.Label(root, textvariable=status_var, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Standby", width=20, command=lambda: set_status("standby")).pack(pady=2)
tk.Button(root, text="Teleop", width=20, command=lambda: set_status("teleop")).pack(pady=2)
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

# === Shutdown Handler ===
def cleanup():
    global running
    print("\nShutting down gracefully...")
    running = False
    time.sleep(0.2)  # Give threads time to stop
    try:
        comm_socket.close()
        print("Socket closed successfully")
    except Exception as e:
        print(f"Error closing socket: {e}")

def on_closing():
    cleanup()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

def signal_handler(sig, frame):
    print("\nCaught Ctrl+C...")
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# === Threads ===
Thread(target=discover_robots, daemon=True).start()
Thread(target=send_controller_data, daemon=True).start()
Thread(target=broadcast_game_status, daemon=True).start()

# === Run GUI ===
try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nInterrupted")
finally:
    cleanup()
