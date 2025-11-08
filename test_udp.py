#!/usr/bin/env python3
"""
Simple UDP broadcast test to diagnose robot discovery issues
Run this to check if UDP broadcasts are working on your network
"""

import socket
import time
import sys

BROADCAST_PORT = 2367

def test_udp_broadcast():
    print("=== UDP Broadcast Test ===")
    print(f"Testing on port {BROADCAST_PORT}\n")
    
    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', BROADCAST_PORT))
    sock.settimeout(2.0)  # 2 second timeout
    
    # Get local IP
    try:
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect(("8.8.8.8", 80))
        local_ip = temp_sock.getsockname()[0]
        temp_sock.close()
        print(f"Your computer's IP: {local_ip}")
        
        # Calculate broadcast address
        ip_parts = local_ip.split('.')
        broadcast_addr = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.255"
        print(f"Broadcast address: {broadcast_addr}")
    except Exception as e:
        print(f"Could not determine IP: {e}")
        broadcast_addr = "255.255.255.255"
        print(f"Using fallback: {broadcast_addr}")
    
    print(f"\nListening on 0.0.0.0:{BROADCAST_PORT}")
    print(f"Broadcasting to {broadcast_addr}:{BROADCAST_PORT}")
    print("\nWhat your robot's IP address? (or press Enter to skip): ", end='')
    robot_ip = input().strip()
    
    if robot_ip:
        print(f"\nRobot IP: {robot_ip}")
        print("Testing direct UDP to robot...")
        try:
            sock.sendto(b"ping", (robot_ip, BROADCAST_PORT))
            print(f"✓ Sent 'ping' directly to {robot_ip}:{BROADCAST_PORT}")
        except Exception as e:
            print(f"✗ Error sending to robot: {e}")
    
    print("\nSending broadcast ping...")
    try:
        sock.sendto(b"ping", (broadcast_addr, BROADCAST_PORT))
        print(f"✓ Sent broadcast 'ping' to {broadcast_addr}:{BROADCAST_PORT}")
    except Exception as e:
        print(f"✗ Error sending broadcast: {e}")
        print("This might be a firewall issue!")
        return
    
    print("\nWaiting for responses (2 seconds)...")
    print("(Your robot should respond with 'pong:RobotName')\n")
    
    received_any = False
    start_time = time.time()
    
    while time.time() - start_time < 2.0:
        try:
            data, addr = sock.recvfrom(1024)
            received_any = True
            print(f"✓ Received from {addr[0]}:{addr[1]}")
            print(f"  Data: {data}")
            if data.startswith(b"pong:"):
                robot_name = data[5:].decode().strip()
                print(f"  🤖 Robot discovered: {robot_name}")
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error receiving: {e}")
            break
    
    if not received_any:
        print("\n✗ No responses received!")
        print("\nPossible issues:")
        print("1. Robot is not on the same network")
        print("2. Robot is not running or not connected to WiFi")
        print("3. Firewall is blocking UDP on port 2367")
        print("4. Router is blocking broadcast packets")
        print("\nTroubleshooting:")
        print("- Check robot's Serial Monitor - is it connected to WiFi?")
        print("- Check if robot received the ping (should print message)")
        print("- Try running: sudo pfctl -d  (to temporarily disable macOS firewall)")
        if robot_ip:
            print(f"- Try pinging the robot: ping {robot_ip}")
    else:
        print("\n✓ UDP communication is working!")
    
    sock.close()

if __name__ == "__main__":
    try:
        test_udp_broadcast()
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

