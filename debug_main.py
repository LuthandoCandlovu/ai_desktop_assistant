import traceback
import sys
import os

print("🚀 Starting AI Desktop Assistant Debug...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

try:
    # Test basic imports
    print("1. Testing imports...")
    import customtkinter as ctk
    print("   ✅ customtkinter imported")
    
    from assistant import AIAssistant
    print("   ✅ AIAssistant imported")
    
    # Test assistant creation
    print("2. Testing assistant creation...")
    assistant = AIAssistant()
    print("   ✅ Assistant created successfully")
    
    # Test GUI creation
    print("3. Testing GUI creation...")
    
    class SimpleApp:
        def __init__(self):
            self.root = ctk.CTk()
            self.root.title("Debug Test")
            self.root.geometry("400x300")
            
            label = ctk.CTkLabel(self.root, text="🎉 AI Desktop Assistant is Working!", font=("Arial", 16))
            label.pack(pady=20)
            
            button = ctk.CTkButton(self.root, text="Test Voice", command=self.test_voice)
            button.pack(pady=10)
            
            exit_btn = ctk.CTkButton(self.root, text="Exit", command=self.root.quit, fg_color="red")
            exit_btn.pack(pady=10)
            
        def test_voice(self):
            print("Voice button clicked!")
            
        def run(self):
            print("4. Starting GUI main loop...")
            self.root.mainloop()
    
    app = SimpleApp()
    app.run()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Full traceback:")
    traceback.print_exc()
    input("Press Enter to exit...")