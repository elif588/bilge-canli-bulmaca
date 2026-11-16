@echo off
chcp 65001 >nul
title Almina Tarot - Canlı Yayın Sistemi
cd /d "c:\Users\CAN\Desktop\tarot"

echo =======================================================
echo 🔮 ALMİNA TAROT CANLI YAYIN SİSTEMİ AÇILIYOR...
echo =======================================================
echo.
echo [1/2] Canlı Yayın Ekranı ve Kontrol Masası açılıyor...
echo [2/2] Tarayıcı ekranları hazırlandı...
echo.

start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8765/panel.html & start http://127.0.0.1:8765/index.html"
python run.py

pause
