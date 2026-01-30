# 📊 Attendance Management System

## Overview

The **Attendance Management System** is a modern, automated attendance tracking application that uses **facial recognition technology** to mark student attendance. It combines computer vision with a user-friendly graphical interface to make attendance marking fast, accurate, and hassle-free.

This system is perfect for schools, colleges, and training centers that want to automate their attendance process.

---

## ✨ Key Features

### 1. **Automated Face Recognition**
   - Uses computer vision to automatically detect and recognize student faces
   - Fast and accurate attendance marking without manual entry
   - Real-time face detection using Haar Cascade classifiers

### 2. **Student Management**
   - Register new students with their enrollment number and name
   - Capture multiple training images for accurate face recognition
   - Manage student details (add, view, edit, delete)
   - Store student data in a secure database

### 3. **Multiple Attendance Methods**
   - **Auto Attendance**: Mark attendance automatically using camera feed
   - **Manual Attendance**: Mark attendance manually for students who couldn't be detected
   - Flexible attendance options for different scenarios

### 4. **Analytics & Reporting**
   - View daily attendance counts
   - Generate attendance reports
   - Analyze attendance trends
   - Export attendance data for further analysis

### 5. **Admin Panel**
   - Secure admin login with authentication
   - Manage all system settings
   - Oversee student registrations
   - View system logs and reports

### 6. **Model Training**
   - Train facial recognition models from student images
   - Improve recognition accuracy with more training images
   - Support for LBPH (Local Binary Patterns Histograms) algorithm

---

## 📁 Project Structure

```
Attendance-Management/
├── main.py                          # Main application entry point
├── config.py                        # Configuration settings
├── StudentDetails.csv               # Student database (CSV format)
├── haarcascade_frontalface_default.xml  # Face detection classifier
│
├── components/                      # Core application modules
│   ├── student_registration.py      # Register new students
│   ├── model_training.py            # Train facial recognition models
│   ├── auto_attendance.py           # Automatic attendance marking
│   ├── auto_attendance_enhanced.py  # Enhanced auto attendance features
│   ├── manual_attendance.py         # Manual attendance marking
│   ├── admin_panel.py               # Admin control panel
│   ├── analytics.py                 # Attendance analytics & reporting
│   ├── dashboard.py                 # Analytics dashboard UI
│   └── face_engine.py               # Face detection & recognition engine
│
├── data/                            # Data handling modules
│   ├── database_handler.py          # CSV database operations
│   └── __init__.py
│
├── utils/                           # Utility modules
│   ├── logger.py                    # Logging functionality
│   ├── validators.py                # Input validation
│   └── __init__.py
│
├── TrainingImage/                   # Folder for storing training images
│   └── (enrollment_number_images)/
│
├── TrainingImageLabel/              # Folder for trained models
│   ├── Trainner.yml                 # Trained face recognition model
│   └── enrollment_map.json          # Mapping of enrollment to labels
│
├── Attendance/                      # Folder for attendance records
│   └── (daily_attendance_csv_files)/
│
└── logs/                            # Application logs
    └── (log_files)/
```

---

## 🎯 How It Works

### 1. **Student Registration**
   - Admin registers a new student with enrollment number and name
   - System captures 5-10 photos of the student's face
   - Images are stored in the `TrainingImage` folder

### 2. **Model Training**
   - Admin trains the facial recognition model
   - System uses LBPH algorithm to create a face model
   - Trained model is saved as `Trainner.yml`

### 3. **Attendance Marking (Automatic)**
   - Webcam captures live video feed
   - Face detection finds faces in the frame
   - Face recognition compares detected faces with trained models
   - Attendance is automatically marked if match is found

### 4. **Attendance Marking (Manual)**
   - Admin manually selects students to mark present
   - Used when automatic detection fails
   - Ensures no student is missed

### 5. **Analytics**
   - View daily attendance summary
   - Check attendance records
   - Export reports for analysis

---

## 💻 Technology Stack

| Technology | Purpose |
|-----------|---------|
| **Python** | Programming language |
| **OpenCV** | Computer vision and face detection |
| **Tkinter** | Graphical User Interface (GUI) |
| **Pandas** | Data manipulation and CSV handling |
| **LBPH Algorithm** | Face recognition model training |

---

## 👥 User Roles

### **Admin**
- Login with admin credentials
- Register students
- Train face recognition models
- View analytics
- Manage system settings

### **User/Staff**
- Mark attendance (auto or manual)
- View attendance reports
- No access to student management

---

## 📊 Data Storage

- **StudentDetails.csv**: Contains enrollment number, name, and other student info
- **Attendance/ folder**: Daily attendance records in CSV format
- **TrainingImage/ folder**: Student face images for model training
- **Trainner.yml**: Trained facial recognition model file
- **enrollment_map.json**: Maps enrollment numbers to face model labels

---

## 🚀 Getting Started

See **Setup.md** for detailed installation and setup instructions.

### Quick Start:
```bash
# 1. Install required packages
pip install -r requirements.txt

# 2. Run the application
python main.py

# 3. Login as Admin
Username: Heeralal
Password: Heera@1234
```

---

## 📖 Requirements

See **requirement.md** for detailed technology requirements and dependencies.

---

## 🔒 Security

- Admin login required for sensitive operations
- Student data stored securely in CSV format
- Face images stored locally on the system
- No external data transmission

---

## 🎨 User Interface

The system features:
- **Dark theme** for comfortable viewing
- **Intuitive navigation** with clear menu options
- **Real-time camera feed** display
- **Interactive dashboards** for analytics
- **Pop-up windows** for different operations

---

## 📝 Common Operations

### Register a Student
1. Click "Register Student" in admin panel
2. Enter enrollment number and name
3. Click "Capture Images"
4. Show your face to camera (5-10 photos will be captured)
5. Click "Done"

### Train Model
1. Click "Train Model" in admin panel
2. System will process all training images
3. Model will be saved automatically

### Mark Attendance
1. Click "Auto Attendance" 
2. Show your face to camera
3. System automatically marks attendance when recognized

---

## 🐛 Troubleshooting

- **Face not recognized**: Capture more training images from different angles
- **Camera not working**: Check camera permissions and try restarting the app
- **Low accuracy**: Retrain the model with more diverse images
- **CSV file errors**: Delete the corrupted file and restart the application

---

## 📞 Support

For issues or questions:
1. Check the logs in the `logs/` folder
2. Review the application error messages
3. Ensure all dependencies are installed correctly

---

## 📄 License

This project is created for educational purposes.

---

**Last Updated**: January 30, 2026
