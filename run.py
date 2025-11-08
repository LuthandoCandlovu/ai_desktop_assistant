import threading
import time
from voice_engine import VoiceEngine
from gesture_control import GestureController
from ai_vision import AIVision
# Import other components as needed

class AIDesktopAssistant:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.gesture_controller = GestureController()
        self.ai_vision = AIVision()
        self.running = True
        
    def start_voice_assistant(self):
        """Start the voice assistant component"""
        try:
            self.voice_engine.listen()
        except Exception as e:
            print(f"Voice assistant error: {e}")
            
    def start_gesture_control(self):
        """Start the gesture control component"""
        try:
            self.gesture_controller.detect_gestures()
        except Exception as e:
            print(f"Gesture control error: {e}")
            
    def run(self):
        """Start all components"""
        print("Starting AI Desktop Assistant...")
        
        # Start components in separate threads
        voice_thread = threading.Thread(target=self.start_voice_assistant)
        gesture_thread = threading.Thread(target=self.start_gesture_control)
        
        voice_thread.daemon = True
        gesture_thread.daemon = True
        
        voice_thread.start()
        gesture_thread.start()
        
        # Keep the main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down AI Desktop Assistant...")
            self.running = False

if __name__ == "__main__":
    assistant = AIDesktopAssistant()
    assistant.run()