# Face Recognition Attendance System

A comprehensive automated attendance management system using face detection, built with Python, OpenCV, MySQL, and Tkinter. Features dual-interface GUI for teachers and students with secure authentication and real-time attendance logging.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### Core Functionality
- **🎥 Automated Face Detection**: Real-time face detection using OpenCV's Haar Cascade Classifier
- **👤 Student Registration**: Capture and store student images with enrollment details
- **📊 Dual Attendance Modes**: 
  - Automatic attendance via face detection
  - Manual attendance entry with validation
- **🔐 Secure Authentication**: User login/signup with bcrypt password hashing
- **💾 Database Persistence**: MySQL database for efficient data storage and retrieval
- **📈 Attendance Tracking**: Complete attendance history with statistics

### Security Features
- Environment-based configuration (no hardcoded credentials)
- Password hashing using bcrypt
- SQL injection prevention with parameterized queries
- Secure file handling

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0 or higher
- Webcam for face detection

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup
1. Start your MySQL server
2. Run the database schema:
```bash
mysql -u root -p < database/schema.sql
```

Or manually create the database:
```sql
CREATE DATABASE attendance_system;
```
Then import the `database/schema.sql` file.

### Step 4: Configuration
1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` with your database credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=attendance_system
```

⚠️ **IMPORTANT**: Never commit your `.env` file to version control!

### Step 5: Run the Application
```bash
cd src
python main.py
```

## 📁 Project Structure

```
face-recognition-attendance/
├── src/
│   ├── main.py                  # Main application interface
│   ├── online_attendance.py     # Automated attendance module
│   ├── manual_attendance.py     # Manual attendance entry
│   ├── login.py                 # User authentication
│   ├── signup.py                # User registration
│   └── db_helper.py             # Database operations helper
├── assets/
│   ├── bg.jpg                   # Background image
│   └── haarcascade_frontalface_default.xml
├── data/
│   ├── images/                  # Stored student images
│   └── temp/                    # Temporary files
├── database/
│   └── schema.sql               # Database structure
├── config.py                    # Application configuration
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 💻 Usage

### Student Registration
1. Launch the main application
2. Enter student's enrollment ID and name
3. Click "Register Student"
4. Look at the camera for 3 seconds
5. Student data and image will be saved

### Online Attendance
1. Click "Online Attendance" from main menu
2. Select the subject
3. Click "Start Attendance"
4. Face detection will begin
5. Press 'P' to stop detection

### Manual Attendance
1. Click "Manual Attendance" from main menu
2. Enter enrollment ID or use auto-fill
3. Select subject and status (Present/Absent)
4. Click "Submit Attendance"

### Check Attendance
1. Click "Check Attendance"
2. Login with your credentials (or signup for new account)
3. View your attendance records

## 🗄️ Database Schema

### Tables
- **students**: Student information and images
- **subjects**: Subject details
- **users**: Authentication credentials
- **attendance**: Attendance records with timestamps

### Views
- **attendance_report**: Detailed attendance records
- **attendance_stats**: Attendance statistics and percentages

## 🔧 Configuration

All configuration is centralized in `config.py`:
- Database credentials (from `.env`)
- File paths
- UI settings
- Face detection parameters

## 🛡️ Security Best Practices

✅ **Implemented:**
- Environment variables for sensitive data
- Password hashing with bcrypt
- Parameterized SQL queries
- Secure file handling
- `.gitignore` for sensitive files

## 📝 To-Do / Future Enhancements

- [ ] Implement actual face recognition (currently uses detection only)
- [ ] Add face encoding storage and matching
- [ ] Generate attendance reports (PDF/Excel export)
- [ ] Add admin dashboard
- [ ] Email notifications for low attendance
- [ ] Multiple face recognition in single frame
- [ ] Attendance analytics and visualizations
- [ ] Mobile app integration

## 🐛 Known Issues

- Face detection currently doesn't identify specific students (recognition not implemented)
- Need to implement face encoding and matching algorithm
- Password verification in login needs bcrypt comparison (currently direct comparison)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Devansh**
- GitHub: [Devansh](https://github.com/anshudevansh)

## 🙏 Acknowledgments

- OpenCV community for face detection algorithms
- Python community for excellent libraries
- MySQL for robust database management

## 📧 Contact

For questions or support, please open an issue or contact [anshudevansh483@gmail.com](mailto:anshudevansh@gmail.com)

---

**⭐ If you find this project useful, please consider giving it a star!**
