import customtkinter as ctk
import threading
import sys
import os
import time

# Import with comprehensive error handling
try:
    from assistant import AIAssistant
    ASSISTANT_AVAILABLE = True
except Exception as e:
    ASSISTANT_AVAILABLE = False
    print(f"Assistant import failed: {e}")

class DesktopAssistantApp:
    def __init__(self):
        self.assistant = None
        self.voice_available = False
        
        if ASSISTANT_AVAILABLE:
            try:
                self.assistant = AIAssistant()
                # Test if voice works without actually speaking
                self.voice_available = hasattr(self.assistant.voice_engine, 'speak')
            except Exception as e:
                print(f"Assistant initialization failed: {e}")
                self.voice_available = False
        else:
            print("Running in text-only mode")
            
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the graphical user interface"""
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("AI Desktop Assistant")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title with status indicator
        status_icon = "🎤" if self.voice_available else "⌨️"
        title_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"🤖 AI Desktop Assistant {status_icon}", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Status
        status_text = "Ready with Voice" if self.voice_available else "Ready (Text Mode)"
        status_color = "green" if self.voice_available else "orange"
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"Status: {status_text}", 
            text_color=status_color,
            font=ctk.CTkFont(size=16)
        )
        self.status_label.pack(pady=10)
        
        # Voice button (only if voice available)
        if self.voice_available:
            self.voice_button = ctk.CTkButton(
                self.main_frame,
                text="🎤 Click to Speak",
                command=self.toggle_listening,
                height=60,
                font=ctk.CTkFont(size=18),
                fg_color="#2E86AB",
                hover_color="#1C6B93"
            )
            self.voice_button.pack(pady=20, fill="x", padx=50)
            self.is_listening = False
        else:
            # Show voice not available message
            voice_msg = ctk.CTkLabel(
                self.main_frame,
                text="Voice disabled - Install PyAudio for voice features",
                text_color="gray",
                font=ctk.CTkFont(size=12)
            )
            voice_msg.pack(pady=10)
        
        # Command entry (always available)
        cmd_frame = ctk.CTkFrame(self.main_frame)
        cmd_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(cmd_frame, text="Type command:").pack(pady=5)
        self.command_entry = ctk.CTkEntry(cmd_frame, placeholder_text="Type command and press Enter...")
        self.command_entry.pack(pady=5, padx=10, fill="x")
        self.command_entry.bind("<Return>", self.process_text_command)
        
        submit_btn = ctk.CTkButton(cmd_frame, text="Submit", command=self.process_text_command)
        submit_btn.pack(pady=5)
        
        # Response display
        response_frame = ctk.CTkFrame(self.main_frame)
        response_frame.pack(fill="both", expand=True, pady=20, padx=20)
        
        response_label = ctk.CTkLabel(
            response_frame, 
            text="Assistant Response:", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        response_label.pack(pady=10)
        
        self.response_text = ctk.CTkTextbox(
            response_frame,
            height=150,
            font=ctk.CTkFont(size=14),
            wrap="word"
        )
        self.response_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.response_text.insert("1.0", "Welcome to AI Desktop Assistant!\n\nType commands like:\n- 'time'\n- 'joke'\n- 'system info'\n- 'open chrome'\n\n")
        self.response_text.configure(state="disabled")
        
        # Quick commands
        self.setup_quick_commands()
        
        # Exit button
        exit_button = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            command=self.exit_app,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            height=40
        )
        exit_button.pack(pady=20)
    
    def setup_quick_commands(self):
        """Setup quick command buttons"""
        commands_frame = ctk.CTkFrame(self.main_frame)
        commands_frame.pack(fill="x", pady=10, padx=20)
        
        commands_label = ctk.CTkLabel(
            commands_frame, 
            text="Quick Commands:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        commands_label.pack(pady=10)
        
        command_buttons = [
            ("Time", "time"),
            ("Date", "date"),
            ("Joke", "joke"),
            ("System Info", "system"),
            ("Screenshot", "screenshot"),
            ("Volume Up", "volume up")
        ]
        
        for i in range(0, len(command_buttons), 3):
            row_frame = ctk.CTkFrame(commands_frame)
            row_frame.pack(fill="x", pady=5)
            
            for j in range(3):
                if i + j < len(command_buttons):
                    text, command = command_buttons[i + j]
                    btn = ctk.CTkButton(
                        row_frame,
                        text=text,
                        command=lambda cmd=command: self.execute_command(cmd),
                        width=120,
                        height=35
                    )
                    btn.pack(side="left", expand=True, padx=5)
    
    def toggle_listening(self):
        """Toggle listening mode (voice only)"""
        if not self.is_listening:
            self.is_listening = True
            self.voice_button.configure(text="🔴 Listening...", fg_color="#E74C3C")
            self.status_label.configure(text="Status: Listening...", text_color="red")
            
            threading.Thread(target=self.listen_for_command, daemon=True).start()
        else:
            self.is_listening = False
            self.voice_button.configure(text="🎤 Click to Speak", fg_color="#2E86AB")
            self.status_label.configure(text="Status: Ready with Voice", text_color="green")
    
    def listen_for_command(self):
        """Listen for voice command"""
        try:
            command = self.assistant.voice_engine.listen()
            if command:
                self.execute_command(command)
        except Exception as e:
            self.show_response(f"Voice error: {str(e)}")
        
        self.is_listening = False
        if self.voice_available:
            self.root.after(0, lambda: self.voice_button.configure(
                text="🎤 Click to Speak", 
                fg_color="#2E86AB"
            ))
            self.root.after(0, lambda: self.status_label.configure(
                text="Status: Ready with Voice", 
                text_color="green"
            ))
    
    def process_text_command(self, event=None):
        """Process text command from entry"""
        command = self.command_entry.get().strip()
        if command:
            self.command_entry.delete(0, "end")
            self.execute_command(command)
    
    def execute_command(self, command):
        """Execute a command and display response"""
        if not self.assistant:
            # Demo mode responses
            responses = {
                "time": f"Current time: {time.strftime('%H:%M:%S')}",
                "date": f"Today's date: {time.strftime('%Y-%m-%d')}",
                "joke": "Why don't scientists trust atoms? Because they make up everything!",
                "system": "System: Windows, Python 3.13, AI Assistant v1.0",
                "screenshot": "Screenshot taken successfully!",
                "hello": "Hello! How can I assist you today?",
                "volume up": "Volume increased!",
                "open chrome": "Opening Google Chrome..."
            }
            response = responses.get(command.lower(), f"I received: '{command}'. Install dependencies for full features.")
            self.show_response(f"You: {command}\n\nAssistant: {response}")
            return
            
        try:
            response = self.assistant.process_command(command)
            self.show_response(f"You: {command}\n\nAssistant: {response}")
            
            # Speak response if voice available
            if self.voice_available and not response.startswith("Error:"):
                self.assistant.voice_engine.speak(response)
                
        except Exception as e:
            self.show_response(f"Error: {str(e)}")
    
    def show_response(self, message):
        """Update response display"""
        self.response_text.configure(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", message)
        self.response_text.configure(state="disabled")
    
    def exit_app(self):
        """Exit the application"""
        self.root.quit()
        self.root.destroy()
        sys.exit()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    if os.name != 'nt':
        print("This application is designed for Windows only.")
        sys.exit(1)
    
    app = DesktopAssistantApp()
    app.run()