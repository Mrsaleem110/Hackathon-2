#!/usr/bin/env python3
"""Monitor backend requests in real-time"""
import subprocess
import time
import sys

print("=" * 70)
print("BACKEND REQUEST MONITOR - Watch for 404/405 errors")
print("=" * 70)
print("\nStarting backend with fresh logs...\n")

# Kill any existing backend process
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
time.sleep(1)

# Start backend
process = subprocess.Popen(
    ['python', 'run_server.py'],
    cwd=r'c:\Users\Chohan Laptop\'s\Documents\GitHub\Hackathon-2\phase_3\backend',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1
)

print("Backend started. Open browser at: http://localhost:5173/login\n")
print("Watching for requests...\n")

try:
    # Monitor output
    while True:
        line = process.stdout.readline()
        if not line:
            break
        
        # Print all request lines
        if 'HTTP/1.1' in line or '404' in line or '405' in line or 'GET' in line or 'POST' in line:
            print(line.rstrip())
            sys.stdout.flush()
            
except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")
    process.terminate()
