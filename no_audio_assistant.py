import customtkinter as ctk
import threading
import time

class NoAudioAssistant:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AI Desktop Assistant (Text Mode)")
        self.root.geometry("500x600")
        
        self.setup_gui()
    
    def setup_gui(self):
        # Title
        title = ctk.CTkLabel(self.root, text="🤖 AI Desktop Assistant", font=("Arial", 24))
        title.pack(pady=20)
        
        # Status
        self.status = ctk.CTkLabel(self.root, text="Status: Ready (Text Mode)", text_color="orange")
        self.status.pack(pady=10)
        
        # Command entry
        cmd_frame = ctk.CTkFrame(self.root)
        cmd_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(cmd_frame, text="Enter Command:").pack(pady=5)
        self.command_entry = ctk.CTkEntry(cmd_frame, placeholder_text="Type your command here...")
        self.command_entry.pack(pady=5, padx=10, fill="x")
        self.command_entry.bind("<Return>", self.process_text_command)
        
        submit_btn = ctk.CTkButton(cmd_frame, text="Submit", command=self.process_text_command)
        submit_btn.pack(pady=5)
        
        # Response area
        self.response_text = ctk.CTkTextbox(self.root, height=300)
        self.response_text.pack(pady=10, padx=20, fill="both", expand=True)
        self.response_text.insert("1.0", "Welcome to AI Desktop Assistant!\n\nType commands like:\n- 'time'\n- 'joke' \n- 'open chrome'\n- 'system info'\n\n")
        
        # Quick commands
        quick_frame = ctk.CTkFrame(self.root)
        quick_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(quick_frame, text="Quick Commands:").pack(pady=5)
        
        commands = [
            ("Time", "time"),
            ("Joke", "joke"), 
            ("System Info", "system"),
            ("Screenshot", "screenshot")
        ]
        
        for text, cmd in commands:
            btn = ctk.CTkButton(quick_frame, text=text, command=lambda c=cmd: self.execute_command(c))
            btn.pack(side="left", padx=5, pady=5)
    
    def process_text_command(self, event=None):
        command = self.command_entry.get().strip()
        if command:
            self.command_entry.delete(0, "end")
            self.execute_command(command)
    
    def execute_command(self, command):
        self.response_text.insert("end", f"\n\nYou: {command}")
        self.status.configure(text="Status: Processing...", text_color="yellow")
        
        # Process in thread to avoid freezing GUI
        threading.Thread(target=self._process_command, args=(command,), daemon=True).start()
    
    def _process_command(self, command):
        try:
            # Simulate processing
            time.sleep(1)
            
            # Simple command responses
            responses = {
                "time": f"Current time is: {time.strftime('%H:%M:%S')}",
                "date": f"Today is: {time.strftime('%Y-%m-%d')}",
                "joke": "Why don't scientists trust atoms? Because they make up everything!",
                "hello": "Hello! How can I assist you today?",
                "system": "System information: Windows, Python 3.13, AI Assistant v1.0",
                "screenshot": "Screenshot taken and saved!",
                "open chrome": "Opening Google Chrome...",
                "weather": "Weather: Sunny, 22°C in your location"
            }
            
            response = responses.get(command.lower(), f"I received your command: '{command}'. This is a text-only demo.")
            
            # Update GUI in main thread
            self.root.after(0, lambda: self._show_response(response))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_response(f"Error: {str(e)}"))
    
    def _show_response(self, response):
        self.response_text.insert("end", f"\nAssistant: {response}")
        self.response_text.see("end")
        self.status.configure(text="Status: Ready (Text Mode)", text_color="orange")
    
    def run(self):
        print("🎉 Starting AI Assistant (Text Mode)...")
        self.root.mainloop()

if __name__ == "__main__":
    app = NoAudioAssistant()
    app.run()