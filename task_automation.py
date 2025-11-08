import pyautogui
import psutil
import os
import webbrowser
import subprocess
from datetime import datetime

class TaskAutomation:
    def __init__(self):
        self.app_paths = {
            'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe'
        }
    
    def open_application(self, app_name):
        """Open specified application"""
        app_name = app_name.lower()
        
        if app_name in self.app_paths:
            try:
                subprocess.Popen(self.app_paths[app_name])
                return f"Opening {app_name}"
            except:
                return f"Could not open {app_name}"
        else:
            return f"Application {app_name} not configured"
    
    def close_application(self, app_name):
        """Close specified application"""
        app_name = app_name.lower()
        
        for process in psutil.process_iter(['name']):
            if app_name in process.info['name'].lower():
                process.terminate()
                return f"Closed {app_name}"
        
        return f"{app_name} not found"
    
    def search_web(self, query):
        """Search the web"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        return f"Searching for {query}"
    
    def system_info(self):
        """Get system information"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""
        💻 System Information:
        CPU Usage: {cpu_percent}%
        Memory: {memory.percent}% used
        Disk: {disk.percent}% used
        """
        return info
    
    def take_screenshot(self):
        """Take screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        return f"Screenshot saved as {filename}"
    
    def volume_control(self, action):
        """Control system volume"""
        if "mute" in action:
            pyautogui.press('volumemute')
            return "Toggled mute"
        elif "up" in action:
            pyautogui.press('volumeup')
            return "Volume increased"
        elif "down" in action:
            pyautogui.press('volumedown')
            return "Volume decreased"
    
    def type_text(self, text):
        """Type text"""
        pyautogui.write(text)
        return f"Typed: {text}"