import speech_recognition as sr
import pyttsx3
import threading
import time

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure voice settings
        voices = self.tts_engine.getProperty('voices')
        self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        self.tts_engine.setProperty('rate', 180)  # Speaking speed
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def speak(self, text):
        """Convert text to speech"""
        def speak_thread():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
    
    def listen(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition: {e}")
            return None
    
    def continuous_listen(self, callback):
        """Continuously listen for wake word"""
        wake_words = ["hey assistant", "hello assistant", "wake up"]
        
        while True:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Background heard: {text}")
                
                if any(word in text for word in wake_words):
                    print("🚀 Wake word detected!")
                    self.speak("Yes, I'm listening. How can I help you?")
                    callback()
                    
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except Exception as e:
                print(f"Error in continuous listen: {e}")
                time.sleep(1)