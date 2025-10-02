@echo off
setlocal enabledelayedexpansion

echo ====================================
echo    YOLO Detection Studio - Setup e Execucao
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

:menu
echo.
echo ====================================
echo           MENU PRINCIPAL  
echo ====================================
echo    1 - Executar YOLO Detection Studio
echo    2 - Configurar/Atualizar Ambiente
echo    3 - Sair
echo.
set /p choice="Digite sua escolha (1, 2 ou 3): "

if "!choice!"=="1" goto executar
if "!choice!"=="2" goto configurar
if "!choice!"=="3" goto sair
echo Opcao invalida!
goto menu

:configurar
echo.
echo ==================================================================
echo Configurando ambiente virtual...
echo ==================================================================

if exist ".venv" (
    echo INFO: Ambiente virtual ja existe.
    echo.
    echo    1 - Usar existente
    echo    2 - Criar novo
    echo.
    set /p venv_choice="Escolha (1 ou 2): "
    if "!venv_choice!"=="2" (
        echo Removendo ambiente existente...
        rmdir /s /q ".venv"
        python -m venv .venv
        echo OK: Novo ambiente criado.
    ) else (
        echo OK: Usando ambiente existente.
    )
) else (
    echo Criando ambiente virtual...
    python -m venv .venv
    echo OK: Ambiente criado.
)

echo.
echo Ativando ambiente e instalando dependencias...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERRO: Falha na instalacao.
    pause
    goto menu
)

echo OK: Configuracao concluida!
pause
goto menu

:executar
echo.
echo ==================================================================
echo Iniciando YOLO Detection Studio...
echo ==================================================================

if not exist ".venv\Scripts\activate.bat" (
    echo ERRO: Ambiente nao configurado. Execute opcao 2 primeiro.
    pause
    goto menu
)

call ".venv\Scripts\activate.bat"
python app.py

echo.
echo Programa encerrado.
pause
goto menu

:sair
echo Saindo...
exit /b 0