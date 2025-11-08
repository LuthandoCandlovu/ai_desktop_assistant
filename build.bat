@echo off
echo Building AI Desktop Assistant for Windows...

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
pip install -r requirements.txt

REM Create executable
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icons/assistant.ico --name "AI_Assistant" main.py

echo Build complete! Check the 'dist' folder for AI_Assistant.exe
pause