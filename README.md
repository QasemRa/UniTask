# 🎓 Django University System

A comprehensive university management system with admin-controlled subject assignments, student enrollments, and plagiarism detection.

---

## 🌟 Features

### For Students:
- ✅ View enrolled subjects with assigned doctors
- ✅ Upload assignments (PDF files)
- ✅ Track submission history
- ✅ Google Classroom-style interface
- ✅ Professional academic theme
- ✅ RTL support for Arabic

### For Doctors:
- ✅ View assigned subjects
- ✅ Access student submissions
- ✅ Automatic plagiarism detection
- ✅ Color-coded similarity warnings
- ✅ Download student files
- ✅ Track student activity

### For Admins:
- ✅ Create and manage subjects
- ✅ Assign doctors to subjects
- ✅ Enroll students in subjects
- ✅ Full control over the system
- ✅ User management

---

## 📋 System Requirements

- Python 3.8+
- Django 6.0.1
- Modern web browser (Chrome, Firefox, Edge, Safari)

---

## 🚀 Quick Start

### 1. Setup Database

```bash
cd mysite
python manage.py makemigrations
python manage.py migrate
```

### 2. Create Admin User

```bash
python manage.py createsuperuser
```

### 3. Create Sample Data (Optional)

```bash
python create_sample_data.py
```

### 4. Run Server

```bash
python manage.py runserver
```

### 5. Access Application

- **Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Database migration guide
- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - Frontend design documentation
- **[TESTING_CHECKLIST.md](TESTING_CHECKLIST.md)** - Comprehensive testing guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details

---

## 🏗️ System Architecture

### Database Models

```
User (Django built-in)
├── Profile (role: student/doctor)
├── Subject (name, description, doctor)
├── Enrollment (student, subject)
└── Submission (student, subject, file, text)
```

### Workflow

1. **Admin** creates subjects and assigns doctors
2. **Admin** enrolls students in subjects
3. **Students** see only their enrolled subjects
4. **Students** upload assignments to specific subjects
5. **Doctors** see only their assigned subjects
6. **Doctors** view submissions from enrolled students
7. **System** automatically detects plagiarism

---

## 👥 User Roles

### Admin
- Full system access
- Create/manage subjects
- Assign doctors to subjects
- Enroll students in subjects
- View all data

### Doctor
- View assigned subjects
- Access student submissions for their subjects
- View plagiarism detection results
- Download student files

### Student
- View enrolled subjects
- Upload assignments
- Track submission history
- See assigned doctors

---

## 🎨 Design Features

- **Professional Theme**: Navy blue and white academic color scheme
- **Google Classroom Style**: Card-based layout for subjects
- **Responsive Design**: Works on desktop, tablet, and mobile
- **RTL Support**: Full Arabic language support
- **Smooth Animations**: Professional hover effects and transitions
- **Visual Indicators**: Color-coded status for assignments and plagiarism

---

## 📊 Key Components

### Student Dashboard
- Subject cards with doctor information
- Assignment upload form
- Submission history
- Statistics overview

### Doctor Dashboard
- Assigned subjects overview
- Student submissions table
- Plagiarism detection results
- Statistics cards

### Admin Panel
- Subject management
- Enrollment management
- User management
- Submission overview

---

## 🔒 Security Features

- User authentication required
- Role-based access control
- Students see only their enrolled subjects
- Doctors see only their assigned subjects
- File upload validation (PDF only, 10MB max)
- CSRF protection

---

## 📁 Project Structure

```
mysite/
├── myapp/
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin configuration
│   ├── urls.py            # URL routing
│   └── utils.py           # Utility functions
├── templates/
│   ├── registration/
│   │   └── login.html     # Login page
│   └── myapp/
│       ├── student.html   # Student dashboard
│       └── doctor.html    # Doctor dashboard
├── static/
│   └── css/
│       └── style.css      # Styles
├── media/                 # Uploaded files
├── manage.py              # Django management
├── create_sample_data.py  # Sample data script
└── README.md              # This file
```

---

## 🔧 Configuration

### Settings (mysite/settings.py)

```python
# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login settings
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
```

---

## 📝 Usage Examples

### Admin: Create Subject

1. Login to admin panel
2. Go to "Subjects" → "Add Subject"
3. Fill in:
   - Name: "Mathematics"
   - Description: "Advanced Mathematics"
   - Doctor: Select a doctor
4. Save

### Admin: Enroll Student

1. Go to "Enrollments" → "Add Enrollment"
2. Select:
   - Student: Choose student
   - Subject: Choose subject
3. Save

### Student: Upload Assignment

1. Login as student
2. Go to "Upload Assignment" section
3. Select subject
4. Choose PDF file
5. Click "Upload"

### Doctor: View Submissions

1. Login as doctor
2. View "Submissions" section
3. See all student submissions
4. Click "View File" to download

---

## 🧪 Testing

### Test Accounts (After running create_sample_data.py)

**Doctors:**
- Username: `dr_ahmed` | Password: `password123`
- Username: `dr_sara` | Password: `password123`
- Username: `dr_khaled` | Password: `password123`

**Students:**
- Username: `student1` | Password: `password123`
- Username: `student2` | Password: `password123`
- Username: `student3` | Password: `password123`

### Run Tests

```bash
python manage.py test
```

---

## 🐛 Troubleshooting

### Issue: Static files not loading

```bash
python manage.py collectstatic
```

### Issue: Database errors

```bash
python manage.py migrate --run-syncdb
```

### Issue: Permission errors on media folder

```bash
# Windows
icacls media /grant Everyone:F

# Linux/Mac
chmod -R 755 media
```

---

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] Assignment deadlines
- [ ] Grading system
- [ ] Student-teacher messaging
- [ ] Calendar integration
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Export reports to PDF
- [ ] Multi-language support
- [ ] Dark mode

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is for educational purposes.

---

## 👨‍💻 Support

For issues or questions:
1. Check the documentation files
2. Review the troubleshooting section
3. Contact system administrator

---

## 📞 Contact

- **Project**: Django University System
- **Version**: 2.0
- **Last Updated**: January 22, 2026

---

## 🙏 Acknowledgments

- Django Framework
- Google Classroom (design inspiration)
- Bootstrap (CSS framework concepts)
- Material Design (color palette)

---

## ⚡ Quick Commands Reference

```bash
# Setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python create_sample_data.py

# Run
python manage.py runserver

# Utilities
python manage.py shell
python manage.py dbshell
python manage.py collectstatic

# Testing
python manage.py test
python manage.py check
```

---

**Happy Learning! 🎓**
