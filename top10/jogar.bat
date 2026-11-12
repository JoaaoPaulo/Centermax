@echo off
rem Abre o servidor e 2 jogadores em janelas separadas (para testar e gravar o video).
if exist executavel\servidor.exe (
  start "SERVIDOR" executavel\servidor.exe 2 5000
  timeout /t 2 >nul
  start "JOGADOR 1" executavel\cliente.exe 127.0.0.1 5000
  start "JOGADOR 2" executavel\cliente.exe 127.0.0.1 5000
) else (
  start "SERVIDOR" python servidor.py 2 5000
  timeout /t 2 >nul
  start "JOGADOR 1" python cliente.py 127.0.0.1 5000
  start "JOGADOR 2" python cliente.py 127.0.0.1 5000
)
