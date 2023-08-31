@echo off
setlocal enabledelayedexpansion

:read_cli_result
    :read_cli_result
    :: Get the system's temporary directory using Python
    for /f %%i in ('python3 -c "import tempfile; print(tempfile.gettempdir())"') do set temp_dir=%%i
    echo Temp Directory: %temp_dir%

    :: Set the result file path
    set result_file_path=%temp_dir%\swiftly_cli_result.txt

    :: Check if the result file exists
    if exist "%result_file_path%" (
        :: Read the result
        for /f "delims=" %%a in ("%result_file_path%") do set result=%%a

        :: Remove the temporary file
        del "%result_file_path%"

        echo "%result_file_path%"

        :: Return the result
        echo !result!
        exit /b 0
    )

    echo Error: Result file not found!
    echo "%result_file_path%"
    exit /b 1
goto :eof