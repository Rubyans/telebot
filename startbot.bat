@echo off

call %~dp0project\Scripts\activate

cd %~dp0project

set TOKEN=5093563379:AAEEglZ3oycvkkPw3Miz_tsYwAi3s-nQUw8

python bot_telegram.py

pause