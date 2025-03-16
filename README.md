Explanation:

How It Works
Detects & Closes Screen Recording Apps

Scans running processes for known screen recorders and terminates them.
Disables Screenshots (PrintScreen Key)

Prevents taking screenshots via keyboard shortcuts.
Checks for Remote Desktop or VNC Connections

Scans for open ports that indicate remote access.
Blurs the Screen if Suspicious Activity is Detected

If a screen recorder is detected, it blurs the screen using OpenCV.
Detects Suspicious Windows (e.g., Snipping Tool, OBS, Screen Recorder)

If such a window is found, a warning is displayed.
Runs in a Loop, Checking Every 5 Seconds

Automatically protects against screen watching in real-time.

Requirements:
psutil → For monitoring processes and killing suspicious ones
numpy → Required for handling images in cv2
opencv-python (cv2) → For blurring the screen
pyautogui → For mouse movements and clicking
pywin32 → For interacting with Windows APIs (detecting open windows, disabling screenshots)

Run the following command in your terminal or command prompt:
pip install -r requirements.txt


How to Use
Run the script in Python.
It will automatically disable screenshots and start monitoring.
If a screen recording app or remote access is detected, it will close the application and blur the screen.
To stop the script, press CTRL + C, and it will restore the PrintScreen function before exiting.
