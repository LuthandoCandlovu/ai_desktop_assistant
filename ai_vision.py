import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract
import time


class AIVision:
    def __init__(self):
        # Set Tesseract path (adjust if needed for your system)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def capture_screen(self):
        """Capture current screen"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    def read_screen_text(self):
        """Read text from screen using OCR"""
        screenshot = self.capture_screen()
        text = pytesseract.image_to_string(screenshot)
        return text
    
    def find_on_screen(self, image_path, confidence=0.8):
        """Find image on screen"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            return location
        except Exception as e:
            print(f"Error finding image: {e}")
            return None
    
    def monitor_activity(self, duration=60):
        """Monitor screen activity"""
        start_time = time.time()
        activities = []
        
        while time.time() - start_time < duration:
            current_app = self.get_active_window()
            screenshot = self.capture_screen()
            
            # Simple activity detection (you can enhance this)
            activities.append({
                'time': time.strftime('%H:%M:%S'),
                'application': current_app,
                'screenshot': screenshot
            })
            
            time.sleep(5)  # Check every 5 seconds [Fixed syntax error]
        
        return activities
    
    def get_active_window(self):
        """Get currently active window"""
        try:
            import win32gui
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except ImportError:
            return "Unknown"