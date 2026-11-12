@echo off
chcp 65001 >nul
echo === Gerando os executaveis do Top 10 ===
python -m pip install pyinstaller
python -m PyInstaller --onefile --distpath executavel servidor.py
python -m PyInstaller --onefile --distpath executavel cliente.py
rmdir /s /q build 2>nul
del /q *.spec 2>nul
echo.
echo === Montando o zip COM executavel ===
powershell -Command "Compress-Archive -Force -Path servidor.py,cliente.py,listas.py,palpite.py,README.md,jogar.bat,executavel -DestinationPath Top10_com_executavel.zip"
echo.
echo Pronto! Arquivo criado: Top10_com_executavel.zip
pause
