#!/bin/bash
# Face Recognition Attendance System - Git Bash Setup Guide
# Commands to run in Git Bash

echo "========================================="
echo "Face Recognition Attendance System"
echo "Git Bash Setup & GitHub Push Guide"
echo "========================================="
echo ""

# Navigate to project directory
echo "Step 1: Navigate to project directory"
echo "Command:"
echo "cd /d/vscode/pythonn/face-recognition-attendance"
echo ""

# Setup Environment
echo "Step 2: Create .env file (if not exists)"
echo "Command:"
echo "cp .env.example .env"
echo "Then edit .env with your MySQL password:"
echo "nano .env  # or use: notepad .env"
echo ""

# Install Dependencies
echo "Step 3: Install Python dependencies"
echo "Command:"
echo "pip install -r requirements.txt"
echo ""

# Database Setup
echo "Step 4: Setup MySQL Database"
echo "Command:"
echo "mysql -u root -p < database/schema.sql"
echo "(Enter your MySQL password when prompted)"
echo ""

# Test Application
echo "Step 5: Test the application"
echo "Commands:"
echo "cd src"
echo "python main.py"
echo "# Test all features, then close the app"
echo "cd .."
echo ""

# Git Setup
echo "========================================="
echo "GitHub Deployment via Git Bash"
echo "========================================="
echo ""

echo "Step 6: Initialize Git repository"
echo "Commands:"
echo "git init"
echo "git add ."
echo "git commit -m 'Initial commit: Face Recognition Attendance System'"
echo ""

echo "Step 7: Create GitHub repository"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: face-recognition-attendance"
echo "3. Description: Automated attendance system using face detection"
echo "4. Choose Private or Public"
echo "5. DO NOT initialize with README"
echo "6. Click 'Create repository'"
echo ""

echo "Step 8: Connect to GitHub and push"
echo "Commands (replace YOUR_USERNAME with your GitHub username):"
echo "git remote add origin https://github.com/YOUR_USERNAME/face-recognition-attendance.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""

echo "========================================="
echo "Quick Reference Commands"
echo "========================================="
echo ""
echo "# Check Git status"
echo "git status"
echo ""
echo "# View commit history"
echo "git log --oneline"
echo ""
echo "# Add more changes later"
echo "git add ."
echo "git commit -m 'Description of changes'"
echo "git push"
echo ""
echo "# View current branch"
echo "git branch"
echo ""
echo "# View remote repository"
echo "git remote -v"
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
