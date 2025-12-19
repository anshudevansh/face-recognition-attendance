@echo off
REM Face Recognition Attendance System - Quick Setup Script
REM This script helps you set up the project quickly

echo ========================================
echo Face Recognition Attendance System
echo Quick Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if MySQL is accessible
echo Checking MySQL connection...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] MySQL command line tools not found in PATH
    echo Make sure MySQL Server is installed and running
    echo You can still continue with manual database setup
) else (
    echo [OK] MySQL tools found
)
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo [OK] .env file created
    echo.
    echo IMPORTANT: Please edit .env file with your database credentials!
    echo File location: %cd%\.env
    echo.
) else (
    echo [OK] .env file already exists
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed successfully
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Git is not installed
    echo To push to GitHub, install Git from: https://git-scm.com/download/win
) else (
    echo [OK] Git is installed
)
echo.

REM Summary
echo ========================================
echo Setup Summary
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your MySQL credentials
echo 2. Start MySQL server
echo 3. Import database schema:
echo    mysql -u root -p ^< database\schema.sql
echo 4. Run the application:
echo    cd src
echo    python main.py
echo.
echo For GitHub deployment:
echo 1. Install Git (if not already installed)
echo 2. Initialize repository: git init
echo 3. Add files: git add .
echo 4. Commit: git commit -m "Initial commit"
echo 5. Create repo on GitHub
echo 6. Push: git push -u origin main
echo.
echo ========================================
echo Setup script completed!
echo ========================================
pause
