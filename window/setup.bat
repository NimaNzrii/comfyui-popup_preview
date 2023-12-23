@echo off

IF EXIST venv (
    echo Deleting existing venv...
    RMDIR /S /Q venv
)

echo Installing PopUp Preview...
python -m venv venv

call .\venv\Scripts\deactivate.bat

call .\venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo installed successfully