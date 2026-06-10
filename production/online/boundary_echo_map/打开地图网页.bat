@echo off
setlocal
set "ROOT=%~dp0..\..\.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
set "URL=http://127.0.0.1:8787/production/online/boundary_echo_map/index.html?v=local-open"
set "NODE=C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
set "SERVER=%~dp0local-map-server.js"

start "Boundary Echo Map Server" /min "%NODE%" "%SERVER%" "%ROOT%"
ping -n 2 127.0.0.1 >nul
start "" "%URL%"

endlocal
