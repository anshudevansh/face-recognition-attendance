# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### Option 1: Automated Setup (Windows)
1. Double-click `setup.bat`
2. Follow the prompts
3. Edit `.env` with your MySQL password
4. Import database: `mysql -u root -p < database\schema.sql`
5. Run: `cd src && python main.py`

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create environment file
copy .env.example .env
# Edit .env with your credentials

# 3. Setup database
mysql -u root -p < database\schema.sql

# 4. Run application
cd src
python main.py
```

## 📁 Key Files

- **config.py** - Application configuration
- **.env** - Your database credentials (create from .env.example)
- **database/schema.sql** - Database structure
- **src/main.py** - Main application entry point

## 🔑 Default Configuration

Database: `attendance_system`  
Host: `localhost`  
Port: `3306` (MySQL default)

## 🆘 Common Issues

**Error: "No module named 'cv2'"**
```bash
pip install opencv-python
```

**Error: "Can't connect to MySQL"**
- Ensure MySQL server is running
- Check credentials in `.env` file
- Verify database exists: `CREATE DATABASE attendance_system;`

**Error: "Permission denied"**
- Run command prompt as administrator
- Check file permissions

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.
