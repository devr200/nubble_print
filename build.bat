@echo off
REM Script per creare l'eseguibile su Windows

echo ===================================
echo Build Nubble Print Client - Windows
echo ===================================
echo.

REM Attiva virtual environment se esiste
if exist venv\Scripts\activate.bat (
    echo Attivazione virtual environment...
    call venv\Scripts\activate.bat
)

REM Verifica PyInstaller
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller non trovato, installazione in corso...
    pip install pyinstaller==6.3.0
)

REM Pulisci build precedenti
echo Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Crea l'eseguibile
echo Creazione eseguibile...
pyinstaller --clean NubblePrintClient.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build completata con successo!
    echo ========================================
    echo.
    echo Eseguibile creato in: dist\NubblePrintClient.exe
    echo.
    echo Per utilizzarlo:
    echo   1. Copia dist\NubblePrintClient.exe dove vuoi
    echo   2. Crea un file .env nella stessa cartella
    echo   3. Esegui NubblePrintClient.exe
    echo.
) else (
    echo.
    echo Errore durante la build
    exit /b 1
)

pause
