@echo off
set "VENV=.venv"

rem Check if venv exists. If it doesn't, create it and install the packages
if exist "%VENV%\" (
    rem Activate that venv
    call %VENV%\Scripts\activate.bat
) else (
    rem Create the venv
    python -m venv --system-site-packages %VENV%

    rem Activate that venv
    call %VENV%\Scripts\activate.bat

    rem Install packages into the venv
    pip install -r requirements.txt

    rem Install Windows specific package
    pip install pywin32
)

rem Launch the tool
python ./main.py

rem Deactivate the venv
call %VENV%\Scripts\deactivate.bat