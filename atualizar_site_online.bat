@echo off
chcp 65001 > nul
echo ======================================================
echo    ATUALIZANDO DASHBOARD CLEAN MASTER ONLINE
echo ======================================================
echo.

cd /d "C:\Users\muril\Desktop\CLEAN MASTER - 2026"

if exist "C:\Users\muril\Desktop\BALANÇA_ATERRO.xlsx" (
    echo [1/3] Copiando planilha atualizada da Area de Trabalho...
    copy /y "C:\Users\muril\Desktop\BALANÇA_ATERRO.xlsx" "C:\Users\muril\Desktop\CLEAN MASTER - 2026\BALANÇA_ATERRO.xlsx" > nul
) else (
    echo [1/3] Usando a planilha da pasta do projeto...
)

echo [2/3] Salvando alteracoes...
git add "BALANÇA_ATERRO.xlsx"
git commit -m "Atualizacao automatica dos dados da balanca" > nul 2>&1

echo [3/3] Enviando dados para o GitHub...
git push origin main

echo.
echo ======================================================
echo    SUCESSO! O portal online vai atualizar sozinho em ~1 min!
echo ======================================================
timeout /t 5
