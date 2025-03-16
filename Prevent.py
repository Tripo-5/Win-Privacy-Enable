import psutil
import socket
import cv2
import numpy as np
import pyautogui
import win32gui
import random
import time
from ctypes import windll

# List of known screen recording software processes
RECORDING_APPS = ["obs.exe", "camstudio.exe", "screencast.exe", "bandicam.exe"]
REMOTE_PORTS = [3389, 5900, 5938]  # RDP, VNC, TeamViewer
SUSPICIOUS_WINDOW_TITLES = ["Snipping Tool", "Screen Recorder", "OBS"]
DETECTION_THRESHOLD = 3  # Prevents repeated spam warnings
detections = {port: 0 for port in REMOTE_PORTS}

def detect_screen_recording():
    """Detect if any screen recording software is running."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] and process.info['name'].lower() in RECORDING_APPS:
            print(f"⚠️ Screen recording detected: {process.info['name']} (PID: {process.info['pid']})")
            return True
    return False

def disable_screenshot():
    """Disable the PrintScreen key to prevent screenshots."""
    windll.user32.RegisterHotKey(None, 1, 0, 0x2C)  # 0x2C is the PrintScreen key
    print("🛑 Screenshot disabled!")

def enable_screenshot():
    """Re-enable the PrintScreen key."""
    windll.user32.UnregisterHotKey(None, 1)
    print("✅ Screenshot enabled!")

def check_remote_access():
    """Detect remote access, but alert only after multiple detections."""
    global detections
    for port in REMOTE_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            detections[port] += 1
            if detections[port] >= DETECTION_THRESHOLD:
                print(f"⚠️ Remote access detected on port {port}!")
                detections[port] = 0  # Reset counter after alert
        else:
            detections[port] = 0  # Reset if not detected
        sock.close()

def blur_screen():
    """Blur the screen to prevent screen watching."""
    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(img, (99, 99), 30)
    cv2.imshow("🔒 Privacy Mode Activated", blurred)
    cv2.waitKey(5000)  # Show the blurred screen for 5 seconds
    cv2.destroyAllWindows()

def detect_suspicious_window():
    """Detect if any suspicious window is open (e.g., Snipping Tool)."""
    def callback(hwnd, extra):
        title = win32gui.GetWindowText(hwnd)
        if any(suspicious in title for suspicious in SUSPICIOUS_WINDOW_TITLES):
            print(f"⚠️ Suspicious window detected: {title}")

    win32gui.EnumWindows(callback, None)

def close_screen_recording():
    """Forcefully close screen recording applications."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'] and process.info['name'].lower() in RECORDING_APPS:
            print(f"❌ Closing {process.info['name']} (PID: {process.info['pid']})")
            psutil.Process(process.info['pid']).terminate()

def move_mouse_and_click():
    """Move the mouse slightly and click in the bottom-left corner every 30-60 seconds."""
    screen_width, screen_height = pyautogui.size()  # Get screen size

    while True:
        # Random small movement
        x, y = pyautogui.position()
        move_x = random.randint(-10, 10)
        move_y = random.randint(-10, 10)
        pyautogui.moveTo(x + move_x, y + move_y, duration=0.5)
        print("🖱️ Mouse moved to prevent 'Away' status.")

        # Click in bottom-left corner (safe spot)
        pyautogui.moveTo(5, screen_height - 5, duration=0.5)  # Move to (5, height-5)
        pyautogui.click()
        print("✅ Clicked in bottom-left corner.")

        time.sleep(random.randint(30, 60))  # Wait between 30-60 seconds

def main():
    print("🔒 Privacy Protection Started...")
    disable_screenshot()

    # Start mouse movement and click thread
    import threading
    mouse_thread = threading.Thread(target=move_mouse_and_click, daemon=True)
    mouse_thread.start()

    while True:
        if detect_screen_recording():
            close_screen_recording()
            blur_screen()
        
        check_remote_access()
        detect_suspicious_window()
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🔄 Restoring settings and exiting...")
        enable_screenshot()
