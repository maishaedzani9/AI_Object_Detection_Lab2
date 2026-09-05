@echo off
python scripts\download_assets.py %*
if errorlevel 1 exit /b %errorlevel%
