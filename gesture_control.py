import cv2
import pyautogui
import numpy as np
import signal
import sys
import threading
import time
from pynput import keyboard

class GestureController:
    def __init__(self):
        self.running = True
        self.current_gesture = None
        self.gesture_cooldown = 0
        
        # Keyboard listener for simulated gestures
        self.listener = None
        self.setup_keyboard_controls()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🎮 Gesture Controller Started (Keyboard Simulation Mode)")
        print("   Press 1-4 for gestures, Q to quit camera, ESC to exit")
    
    def setup_keyboard_controls(self):
        """Setup keyboard controls to simulate gestures"""
        def on_press(key):
            try:
                if key == keyboard.Key.esc:
                    self.running = False
                    return False
                
                if hasattr(key, 'char') and key.char:
                    if key.char == '1':
                        self._execute_gesture("thumbs_up")
                    elif key.char == '2':
                        self._execute_gesture("thumbs_down")
                    elif key.char == '3':
                        self._execute_gesture("peace_sign")
                    elif key.char == '4':
                        self._execute_gesture("fist")
            except AttributeError:
                pass
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()
    
    def signal_handler(self, sig, frame):
        """Handle interrupt signal gracefully"""
        print("\nShutting down gracefully...")
        self.running = False
        if self.listener:
            self.listener.stop()
    
    def detect_gestures(self):
        """Show camera feed with gesture simulation"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture image")
                    break
                
                frame = cv2.flip(frame, 1)
                
                # Display instructions
                self._display_instructions(frame)
                
                # Show current gesture status
                if self.current_gesture:
                    cv2.putText(frame, f"Last Gesture: {self.current_gesture}", 
                               (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                cv2.imshow('Gesture Control - Press Q to close camera', frame)
                
                # Check for 'q' key press to exit camera (but keep running)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            if self.listener:
                self.listener.stop()
            print("Gesture controller shut down successfully")
    
    def _display_instructions(self, frame):
        """Display instructions on the frame"""
        cv2.putText(frame, "Gesture Control Simulation", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 1: Thumbs Up (Volume Up)", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Press 2: Thumbs Down (Volume Down)", (10, 85), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Press 3: Peace Sign (Screenshot)", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Press 4: Fist (Mouse Click)", (10, 135), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "Python 3.13: Using keyboard simulation", (10, 170), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(frame, "Install Python 3.11 for hand tracking", (10, 190), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    
    def _execute_gesture(self, gesture):
        """Execute action based on recognized gesture"""
        try:
            self.current_gesture = gesture
            
            if gesture == "thumbs_up":
                pyautogui.press('volumeup')
                print("👍 Volume Up")
            
            elif gesture == "thumbs_down":
                pyautogui.press('volumedown')
                print("👎 Volume Down")
            
            elif gesture == "peace_sign":
                screenshot_name = f"gesture_screenshot_{int(time.time())}.png"
                pyautogui.screenshot(screenshot_name)
                print(f"✌️ Screenshot saved as {screenshot_name}")
            
            elif gesture == "fist":
                pyautogui.click()
                print("✊ Mouse Click")
                
        except Exception as e:
            print(f"Error executing gesture: {e}")

    def run_headless(self):
        """Run without camera for background gesture control"""
        print("🎮 Running in headless mode...")
        print("Press 1-4 for gestures, ESC to exit")
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False


if __name__ == "__main__":
    controller = GestureController()
    
    # Auto-start with camera mode
    print("Starting in Camera Mode...")
    controller.detect_gestures()