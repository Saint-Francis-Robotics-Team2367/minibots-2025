# Troubleshooting Robot Discovery Issues

## Quick Diagnostic Steps

### 1. Check Robot Connection
First, make sure your robot is connected to the WiFi network:

1. Open Arduino IDE and connect to your robot
2. Open **Serial Monitor** (Tools → Serial Monitor)
3. You should see:
   ```
   Connecting to WiFi...
   Connected! IP: 192.168.x.x
   Listening on UDP port 2367
   ```
4. **Write down the robot's IP address!**

### 2. Test UDP Communication
Run the diagnostic script:

```bash
python test_udp.py
```

This will:
- Show your computer's IP and broadcast address
- Let you test direct communication to the robot
- Try broadcasting pings
- Show any responses received

### 3. Install Required Python Packages
Make sure you have the required packages:

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install pygame netifaces
```

## Common Issues and Solutions

### Issue: "No robots discovered"

**Possible Causes:**

1. **Robot not on WiFi**
   - Check Serial Monitor on robot
   - Make sure it says "Connected! IP: ..."
   - Verify WiFi credentials in `minibot.h` match your network

2. **Computer and robot on different networks**
   - Both must be on the same WiFi network (WATCHTOWER)
   - Check your computer's WiFi connection

3. **Firewall blocking UDP**
   - macOS: Go to System Preferences → Security & Privacy → Firewall
   - Click "Firewall Options"
   - Make sure Python is allowed
   - Or temporarily disable: `sudo pfctl -d`

4. **Port 2367 already in use**
   - Another program might be using the port
   - Try: `lsof -i :2367` to see what's using it
   - Kill the process or change the port

### Issue: Robot receives pings but doesn't respond

**Check Serial Monitor on Robot:**
- Upload the updated `minibot.cpp` with debugging
- You should see messages like:
  ```
  Received packet (4 bytes) from 192.168.1.100:2367
  Text packet: ping
  Received PING! Sending PONG response...
  Sent pong response: pong:YourRobotName
  ```

**If you see "Received packet" but no "Received PING!":**
- The packet might be corrupted or have extra characters
- Check that the ping is exactly 4 bytes: `ping`

**If you don't see any "Received packet" messages:**
- Robot is not receiving broadcasts
- Check router settings (some routers block broadcasts)
- Try direct IP communication instead

### Issue: "Error closing socket" when pressing Ctrl+C

This was a bug that has been fixed. Update to the latest `driverStation.py`:
- The new version properly shuts down threads before closing the socket

### Issue: Robot found once but not again

This was a bug in older versions where the robot only responded to the first ping. Update `minibot.cpp` to the latest version where the condition `&& !connected` has been removed from the ping response.

## Network Configuration Issues

### Same Subnet Check
Your computer and robot must be on the same subnet:

**Computer IP:** `192.168.1.100` ← Third number
**Robot IP:** `192.168.1.50` ← Must match

If they don't match (e.g., `192.168.0.x` vs `192.168.1.x`), they can't communicate via broadcast.

### Broadcast Address
The broadcast address should be:
- For `192.168.1.x` network → `192.168.1.255`
- For `192.168.0.x` network → `192.168.0.255`

The driver station now auto-detects this, but you can verify it's correct in the console output when starting the driver station.

## Testing Direct Communication

If broadcast isn't working, you can modify the driver station to use direct IP:

1. Get robot's IP from Serial Monitor
2. In `driverStation.py`, change the discover_robots function:

```python
# Instead of:
comm_socket.sendto(b"ping", (broadcast_addr, BROADCAST_PORT))

# Use:
comm_socket.sendto(b"ping", ("192.168.1.50", BROADCAST_PORT))  # Robot's IP
```

This bypasses broadcast and sends directly to the robot.

## Advanced Debugging

### Packet Capture
To see exactly what's being sent/received:

```bash
# Install tcpdump if not already installed
# Then capture UDP traffic on port 2367:
sudo tcpdump -i any -n udp port 2367 -X
```

This will show all UDP packets on that port, helping you verify:
- Are pings being sent?
- Are pongs being received?
- What data is in the packets?

### Check Firewall Rules (macOS)

```bash
# Check if firewall is running
sudo pfctl -s info

# Temporarily disable (for testing only!)
sudo pfctl -d

# Re-enable
sudo pfctl -e
```

### Check Port Availability

```bash
# See what's using port 2367
lsof -i :2367

# Or
netstat -an | grep 2367
```

## Still Having Issues?

1. Check both robot Serial Monitor AND driver station console output
2. Run `test_udp.py` and share the output
3. Verify both devices are on the same network
4. Try the direct IP method instead of broadcast
5. Check router settings for broadcast/multicast blocking
6. Temporarily disable firewall for testing

## Success Checklist

✅ Robot connected to WiFi (Serial Monitor shows IP)
✅ Computer on same WiFi network
✅ Python packages installed (`pygame`, `netifaces`)
✅ Port 2367 not in use by other programs
✅ Firewall allows Python/UDP
✅ `test_udp.py` receives responses
✅ Driver station shows "Discovered new robot" message

