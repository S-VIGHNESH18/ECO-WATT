@echo off
echo Starting GreenFuture Web Application...
cd /d "%~dp0"
start http://127.0.0.1:5173
npm.cmd run dev -- --host 127.0.0.1 --port 5173
pause
