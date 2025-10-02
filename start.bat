@echo off
setlocal enabledelayedexpansion

echo ====================================
echo    YOLO Detection Studio - Launcher
echo ====================================
echo.

REM Verificar Python
echo Verificando instalacao do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo OK: Python encontrado.

echo.
echo ====================================
echo      Configurando Ambiente
echo ====================================

REM Criar ambiente virtual se nao existir
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao criar ambiente virtual.
        pause
        exit /b 1
    )
    echo OK: Ambiente virtual criado.
) else (
    echo OK: Ambiente virtual ja existe.
)

echo.
echo Ativando ambiente virtual...
call ".venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo ERRO: Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)

echo.
echo Atualizando pip...
python -m pip install --upgrade pip --quiet

echo.
echo Instalando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ERRO: Falha na instalacao das dependencias.
    pause
    exit /b 1
)

echo OK: Todas as dependencias instaladas com sucesso!

echo.
echo ====================================
echo   Iniciando YOLO Detection Studio
echo ====================================

python app.py

echo.
echo Programa encerrado.
pause