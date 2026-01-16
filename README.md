# ?? Attendance Management System - Facial Recognition

## ?? Project Overview

The **Attendance Management System** is a fully automated attendance tracking solution using real-time facial recognition technology. It eliminates manual attendance processes, prevents proxy attendance, and provides administrators with comprehensive attendance analytics and reporting.

**Status**: ? Production Ready | **Version**: 2.0 Enhanced

---

## ?? Key Features

### ?? Security & Access Control
- **Admin Login System**: Secure authentication with admin-only features
- **Admin-Only Registration**: Only administrators can register new students
- **Role-Based Access**: Different features for admin and regular users
- **Secure Credentials**: Admin credentials managed through config.py

### ?? Student Management
- **Face Registration**: Capture **30 high-quality images** per student for optimal model training
- **Enrollment ID & Details**: Store complete student information (ID, name, class)
- **Efficient Training**: Optimized model training with reduced images for faster processing

### ?? Attendance Marking
- **Auto-Attendance Mode**: Continuous real-time face recognition
  - Automatically recognizes students walking past the camera
  - Displays personalized "Thank You, [Name]!" message on camera feed
  - Auto-clears message after 2 seconds, continues scanning
  - Press **Q key** only when completely done
  - 100% hands-free operation
  
- **Manual Attendance Mode**: Mark attendance manually for specific scenarios
  - Batch attendance marking
  - Excel/CSV export support

### ?? Analytics & Reporting
- **Real-Time Dashboard**: View student count, marked attendance, pending students
- **Attendance Reports**: Generate Excel files (.xlsx) with:
  - Individual session sheets
  - Summary sheet with complete records
  - Professional formatting (bold headers, colors, auto-width columns)
  - Timestamp and date information

### ????? Admin Features
- **Admin Dashboard**: Central control panel for all operations
- **User Analytics**: View attendance trends and statistics
- **Report Download**: Export attendance as Excel workbooks
- **Student Management**: Register new students (admin only)
- **Model Training**: Train/retrain the facial recognition model
- **System Logs**: Track all operations and errors

---

## ??? Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.13 |
| **GUI Framework** | Tkinter |
| **Face Detection** | OpenCV (Viola-Jones Algorithm) |
| **Face Recognition** | LBPH (Local Binary Patterns Histograms) |
| **Data Storage** | CSV files |
| **Data Processing** | Pandas |
| **Image Processing** | OpenCV, Pillow |
| **Excel Export** | openpyxl |
| **Logging** | Custom logger |

---

## ?? Requirements

pip install -r requirements.txt

---

## ?? Quick Start

python main.py

---

## ?? Admin Credentials

Username: Heeralal
Password: Heera@1234

?? **IMPORTANT**: Change these credentials in config.py for production use!

---

**Last Updated**: January 2026 | **Status**: ? Production Ready
