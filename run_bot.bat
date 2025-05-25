@echo off
REM —— Etiqueta de inicio para el bucle
:start

REM —— Cambia al directorio de tu bot
cd /d F:\Codes\CODEVS\TG-BOT

REM —— Activa tu entorno virtual
call venv\Scripts\activate

REM —— Inicia el bot
python main.py

REM —— Si main.py termina por cualquier razón, espera 10 s y reinicia
timeout /t 10 /nobreak
goto :start
