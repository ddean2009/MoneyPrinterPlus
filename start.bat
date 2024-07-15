chcp 65001
@echo off

IF EXIST venv (
    echo venv dir exist
    call .\venv\Scripts\deactivate.bat

    call .\venv\Scripts\activate.bat
) ELSE (
    echo venv dir not exist
)

REM Check if the batch was started via double-click
IF /i "%%comspec%% /c %%~0 " equ "%%cmdcmdline:"=%%" (
    REM echo This script was started by double clicking.
    cmd /k streamlit run gui.py %*
) ELSE (
    REM echo This script was started from a command prompt.
    streamlit run gui.py %*
)

