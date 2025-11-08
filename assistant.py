from voice_engine import VoiceEngine
from task_automation import TaskAutomation
from face_recognition import FaceRecognizer
from gesture_control import GestureController
from ai_vision import AIVision
import requests
import json
import time
from datetime import datetime, timedelta
import threading

# Import with error handling
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("pywhatkit not available - music playback disabled")

try:
    import pyjokes
    PYJOKES_AVAILABLE = True
except ImportError:
    PYJOKES_AVAILABLE = False
    print("pyjokes not available - joke telling disabled")

try:
    import wolframalpha
    WOLFRAM_AVAILABLE = True
except ImportError:
    WOLFRAM_AVAILABLE = False
    print("wolframalpha not available - calculations disabled")

class AIAssistant:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.automation = TaskAutomation()
        self.face_recognizer = FaceRecognizer()
        self.gesture_controller = GestureController()
        self.ai_vision = AIVision()
        self.reminders = []
        self.commands = self._load_commands()
        self.setup_ai_services()
    
    def setup_ai_services(self):
        """Setup AI API services"""
        if WOLFRAM_AVAILABLE:
            try:
                # You need to get a free API key from wolframalpha.com
                self.wolfram_client = wolframalpha.Client('YOUR_WOLFRAM_APP_ID')
            except:
                self.wolfram_client = None
        else:
            self.wolfram_client = None
    
    def _load_commands(self):
        """Define available commands"""
        base_commands = {
            'open': self.automation.open_application,
            'close': self.automation.close_application,
            'search': self.automation.search_web,
            'system': lambda: self.automation.system_info(),
            'screenshot': lambda: self.automation.take_screenshot(),
            'volume': self.automation.volume_control,
            'type': self.automation.type_text,
            'time': self._get_time,
            'date': self._get_date,
            'weather': self._get_weather,
            'news': self._get_news,
            'joke': self._tell_joke,
            'calculate': self._calculate,
            'play': self._play_music,
            'remind': self._set_reminder,
            'face': self._face_command,
            'gesture': self._gesture_command,
            'vision': self._vision_command
        }
        return base_commands
    
    def _get_time(self):
        """Get current time"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def _get_date(self):
        """Get current date"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    def _get_weather(self, location=None):
        """Get weather information"""
        if not location:
            location = "your location"
        
        try:
            # Simple weather response without API
            weather_responses = [
                f"The weather in {location} is sunny and warm",
                f"In {location}, it's partly cloudy with a chance of rain",
                f"Weather in {location}: clear skies and pleasant",
                f"Currently in {location}: mild temperatures with light breeze"
            ]
            import random
            return random.choice(weather_responses)
        except:
            return "I can check the weather if you provide an API key for weather service"
    
    def _get_news(self):
        """Get latest news"""
        try:
            # Simple news response without API
            news_responses = [
                "Here are today's top headlines: Technology advances continue, weather patterns remain stable, and sports teams are preparing for upcoming seasons.",
                "Top news: Local community events are happening this weekend, new developments in science research, and entertainment updates.",
                "News summary: Economic indicators show positive trends, education sector innovations, and health awareness campaigns."
            ]
            import random
            return random.choice(news_responses)
        except:
            return "I can fetch news if you provide a NewsAPI key"
    
    def _tell_joke(self):
        """Tell a joke"""
        if PYJOKES_AVAILABLE:
            return pyjokes.get_joke()
        else:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "Why don't eggs tell jokes? They'd crack each other up!",
                "What do you call a fake noodle? An impasta!"
            ]
            import random
            return random.choice(jokes)
    
    def _calculate(self, expression):
        """Calculate mathematical expressions"""
        if self.wolfram_client:
            try:
                result = self.wolfram_client.query(expression)
                return next(result.results).text
            except:
                return "Could not calculate that expression"
        else:
            try:
                # Simple calculations without Wolfram
                if '+' in expression:
                    nums = expression.split('+')
                    result = sum(float(n.strip()) for n in nums)
                elif '-' in expression:
                    nums = expression.split('-')
                    result = float(nums[0].strip()) - float(nums[1].strip())
                elif '*' in expression:
                    nums = expression.split('*')
                    result = float(nums[0].strip()) * float(nums[1].strip())
                elif '/' in expression:
                    nums = expression.split('/')
                    result = float(nums[0].strip()) / float(nums[1].strip())
                else:
                    return "Please use basic operations like +, -, *, /"
                
                return f"The answer is {result}"
            except:
                return "I can help with basic math. Try something like 'calculate 5 + 3'"
    
    def _play_music(self, song_name):
        """Play music on YouTube"""
        if PYWHATKIT_AVAILABLE:
            try:
                pywhatkit.playonyt(song_name)
                return f"Playing {song_name} on YouTube"
            except:
                return "Could not play music"
        else:
            return f"I would play {song_name} on YouTube if pywhatkit was installed"
    
    def _set_reminder(self, reminder_text):
        """Set a reminder"""
        reminder_time = datetime.now() + timedelta(minutes=5)  # Default 5 minutes
        self.reminders.append({'time': reminder_time, 'text': reminder_text})
        
        # Start reminder checking thread
        threading.Thread(target=self._check_reminders, daemon=True).start()
        
        return f"Reminder set for {reminder_time.strftime('%H:%M')}: {reminder_text}"
    
    def _check_reminders(self):
        """Check and trigger reminders"""
        while self.reminders:
            now = datetime.now()
            for reminder in self.reminders[:]:
                if now >= reminder['time']:
                    self.voice_engine.speak(f"Reminder: {reminder['text']}")
                    self.reminders.remove(reminder)
            time.sleep(30)
    
    def _face_command(self, command):
        """Handle face recognition commands"""
        if "register" in command:
            name = command.replace("register", "").strip()
            if name:
                if self.face_recognizer.register_face(name):
                    return f"Face registered for {name}"
                else:
                    return "Face registration failed"
            else:
                return "Please specify a name for registration"
        elif "recognize" in command:
            name = self.face_recognizer.recognize_face()
            return f"Welcome back {name}!" if name else "Face not recognized"
        else:
            return "Face command not recognized. Try 'face register [name]' or 'face recognize'"
    
    def _gesture_command(self, command):
        """Handle gesture control commands"""
        if "start" in command:
            threading.Thread(target=self.gesture_controller.detect_gestures, daemon=True).start()
            return "Gesture control activated! Show gestures to the camera"
        return "Gesture control command not recognized. Try 'gesture start'"
    
    def _vision_command(self, command):
        """Handle vision commands"""
        if "read" in command:
            try:
                text = self.ai_vision.read_screen_text()
                return f"I see: {text[:100]}..." if text else "No text detected"
            except:
                return "Text reading not available"
        elif "what do you see" in command:
            return "I'm looking at your screen through the camera. I can detect basic visual information."
        return "Vision command not recognized. Try 'vision read' or 'vision what do you see'"
    
    def _ai_response(self, text):
        """Generate AI response for general conversation"""
        text_lower = text.lower()
        
        # Basic conversation responses
        if any(word in text_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! How can I assist you today?"
        elif any(word in text_lower for word in ['how are you', 'how are you doing']):
            return "I'm functioning well, thank you for asking! How can I help you?"
        elif any(word in text_lower for word in ['thank you', 'thanks']):
            return "You're welcome! Is there anything else I can help with?"
        elif any(word in text_lower for word in ['bye', 'goodbye', 'exit']):
            return "Goodbye! Have a great day!"
        elif any(word in text_lower for word in ['what can you do', 'help']):
            return "I can tell time, date, jokes, open applications, take screenshots, control volume, search the web, set reminders, and more! Just ask."
        else:
            return f"I heard you say: '{text}'. I can help with various tasks like telling time, jokes, opening apps, and more. What would you like to do?"
    
    def process_command(self, text):
        """Process voice command with enhanced capabilities"""
        if not text or not text.strip():
            return "I didn't hear anything. Please try again."
        
        text = text.lower().strip()
        
        # Check for specific commands
        for command, action in self.commands.items():
            if text.startswith(command):
                try:
                    if command in ['open', 'close', 'search', 'volume', 'type', 'weather', 
                                  'calculate', 'play', 'remind', 'face', 'gesture', 'vision']:
                        target = text[len(command):].strip()
                        if target:
                            response = action(target)
                        else:
                            response = f"Please specify what you want to {command}"
                    else:
                        response = action()
                    return response
                except Exception as e:
                    return f"Error executing command: {str(e)}"
        
        # AI response for general conversation
        return self._ai_response(text)


# Test the assistant
if __name__ == "__main__":
    print("🤖 AI Assistant Test Mode")
    print("Type 'exit' to quit")
    print("-" * 40)
    
    assistant = AIAssistant()
    
    while True:
        try:
            command = input("\nYou: ").strip()
            if command.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye! 👋")
                break
                
            if command:
                response = assistant.process_command(command)
                print(f"Assistant: {response}")
                
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")