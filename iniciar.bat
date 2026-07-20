@echo off
title Draco AI - Inicializador

echo.
echo ==========================================
echo             DRACO AI
echo          Inicializando...
echo ==========================================
echo.


cd /d "D:\Draco AI"



echo [1/4] Ativando ambiente virtual...

call .venv\Scripts\activate



echo.
echo [2/4] Iniciando servidor Draco API...
echo.


start "Draco API" cmd /k "cd /d D:\Draco AI && call .venv\Scripts\activate && uvicorn main:app --reload"



echo.
echo Aguardando API iniciar...
timeout /t 5 >nul



echo.
echo [3/4] Iniciando servidor Frontend...
echo.


start "Draco Frontend" cmd /k "cd /d D:\Draco AI\frontend && python -m http.server 5500"



echo.
echo Aguardando Frontend iniciar...
timeout /t 3 >nul



echo.
echo [4/4] Abrindo interface Draco AI...
echo.


start "" "http://localhost:5500"



echo.
echo ==========================================
echo          DRACO AI ONLINE
echo ==========================================
echo.
echo Frontend:
echo http://localhost:5500
echo.
echo API:
echo http://127.0.0.1:8000
echo.
echo Swagger:
echo http://127.0.0.1:8000/docs
echo.
echo ==========================================
echo.
echo Mantenha as janelas abertas.
echo.



pause