@echo off
setlocal

if "%1"=="" goto usage
if "%1"=="phase_1" goto phase_1
if "%1"=="phase_2" goto phase_2
if "%1"=="phase_3" goto phase_3
if "%1"=="phase_4" goto phase_4
if "%1"=="list" goto list
if "%1"=="status" goto status

goto usage

:phase_1
git checkout main
git rev-parse --verify phase_1 >nul 2>&1
if errorlevel 1 (
    echo Creating new branch for phase_1...
    git checkout -b phase_1
) else (
    echo Switching to phase_1 branch...
    git checkout phase_1
)
goto end

:phase_2
git checkout main
git rev-parse --verify phase_2 >nul 2>&1
if errorlevel 1 (
    echo Creating new branch for phase_2...
    git checkout -b phase_2
) else (
    echo Switching to phase_2 branch...
    git checkout phase_2
)
goto end

:phase_3
git checkout main
git rev-parse --verify phase_3 >nul 2>&1
if errorlevel 1 (
    echo Creating new branch for phase_3...
    git checkout -b phase_3
) else (
    echo Switching to phase_3 branch...
    git checkout phase_3
)
goto end

:phase_4
git checkout main
git rev-parse --verify phase_4 >nul 2>&1
if errorlevel 1 (
    echo Creating new branch for phase_4...
    git checkout -b phase_4
) else (
    echo Switching to phase_4 branch...
    git checkout phase_4
)
goto end

:list
echo Available branches:
git branch -a
goto end

:status
echo Current branch:
git branch --show-current
echo Git status:
git status
goto end

:usage
echo Usage: %0 {phase_1^|phase_2^|phase_3^|phase_4^|list^|status}
echo.
echo Commands:
echo   phase_1   - Switch to or create phase_1 branch
echo   phase_2   - Switch to or create phase_2 branch
echo   phase_3   - Switch to or create phase_3 branch
echo   phase_4   - Switch to or create phase_4 branch
echo   list      - List all branches
echo   status     - Show current branch and status
goto end

:end