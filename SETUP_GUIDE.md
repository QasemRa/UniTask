# 🚀 Setup Guide - Django University System

## Complete Setup Instructions for Admin-Controlled Subject Assignment

---

## 📋 Prerequisites

- Python 3.8 or higher
- Django 6.0.1
- Virtual environment (recommended)

---

## 🔧 Installation Steps

### Step 1: Activate Virtual Environment

```bash
# Navigate to project directory
cd mysite

# Activate virtual environment (if using one)
# Windows:
Scripts\activate

# Linux/Mac:
source bin/activate
```

### Step 2: Install Dependencies

```bash
pip install django==6.0.1
pip install sqlparse
```

### Step 3: Create Database Migrations

```bash
python manage.py makemigrations
```

Expected output:
```
Migrations for 'myapp':
  myapp/migrations/0001_initial.py
    - Create model Profile
    - Create model Subject
    - Create model Enrollment
    - Create model Submission
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@university.edu
Password: ********
Password (again): ********
```

### Step 6: Create Media Directory

```bash
# Windows
mkdir media

# Linux/Mac
mkdir -p media
```

---

## 👥 Creating Users and Profiles

### Method 1: Via Admin Panel (Recommended)

1. **Start the server:**
```bash
python manage.py runserver
```

2. **Access admin panel:**
   - URL: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

3. **Create Doctor Users:**
   - Go to "Users" → "Add User"
   - Username: `doctor1`
   - Password: Set password
   - Save
   - Go to "User Profiles" → "Add User Profile"
   - User: Select `doctor1`
   - Role: Select "Doctor"
   - Save

4. **Create Student Users:**
   - Go to "Users" → "Add User"
   - Username: `student1`
   - Password: Set password
   - Save
   - Go to "User Profiles" → "Add User Profile"
   - User: Select `student1`
   - Role: Select "Student"
   - Save

### Method 2: Via Django Shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from myapp.models import Profile

# Create Doctor
doctor = User.objects.create_user(
    username='doctor1',
    password='password123',
    first_name='محمد',
    last_name='أحمد'
)
Profile.objects.create(user=doctor, role='doctor')

# Create Student
student = User.objects.create_user(
    username='student1',
    password='password123',
    first_name='علي',
    last_name='حسن'
)
Profile.objects.create(user=student, role='student')

print("Users created successfully!")
```

---

## 📚 Setting Up Subjects

### Via Admin Panel:

1. **Go to "Subjects" → "Add Subject"**

2. **Create subjects:**

   **Subject 1:**
   - Name: `الرياضيات`
   - Description: `مادة الرياضيات للفصل الدراسي الأول`
   - Doctor: Select `doctor1`
   - Save

   **Subject 2:**
   - Name: `الفيزياء`
   - Description: `مادة الفيزياء للفصل الدراسي الأول`
   - Doctor: Select `doctor1` (or create another doctor)
   - Save

   **Subject 3:**
   - Name: `الكيمياء`
   - Description: `مادة الكيمياء للفصل الدراسي الأول`
   - Doctor: Select a doctor
   - Save

### Via Django Shell:

```python
from django.contrib.auth.models import User
from myapp.models import Subject

doctor = User.objects.get(username='doctor1')

subjects = [
    {'name': 'الرياضيات', 'description': 'مادة الرياضيات'},
    {'name': 'الفيزياء', 'description': 'مادة الفيزياء'},
    {'name': 'الكيمياء', 'description': 'مادة الكيمياء'},
]

for subj_data in subjects:
    Subject.objects.create(
        name=subj_data['name'],
        description=subj_data['description'],
        doctor=doctor
    )

print("Subjects created!")
```

---

## 🎓 Enrolling Students in Subjects

### Via Admin Panel:

1. **Go to "Enrollments" → "Add Enrollment"**

2. **Enroll students:**
   - Student: Select `student1`
   - Subject: Select `الرياضيات`
   - Save
   
   - Repeat for other subjects

### Via Django Shell:

```python
from django.contrib.auth.models import User
from myapp.models import Subject, Enrollment

student = User.objects.get(username='student1')
subjects = Subject.objects.all()

for subject in subjects:
    Enrollment.objects.create(
        student=student,
        subject=subject
    )

print(f"Enrolled {student.username} in {subjects.count()} subjects")
```

---

## 🧪 Testing the System

### 1. Test Student Login

1. Logout from admin
2. Go to: http://127.0.0.1:8000/
3. Login with:
   - Username: `student1`
   - Password: `password123`
4. You should see:
   - Enrolled subjects in cards
   - Doctor names
   - Upload form
   - Empty submissions list

### 2. Test File Upload

1. As student, go to "Upload Assignment" section
2. Select a subject
3. Choose a PDF file
4. Click "Upload"
5. You should see success message
6. Assignment appears in submissions list

### 3. Test Doctor Login

1. Logout
2. Login with:
   - Username: `doctor1`
   - Password: `password123`
3. You should see:
   - Assigned subjects
   - Student submissions
   - Statistics
   - Plagiarism detection (if 2+ submissions)

---

## 📊 Sample Data Script

Create a file `mysite/create_sample_data.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import Profile, Subject, Enrollment

def create_sample_data():
    print("Creating sample data...")
    
    # Create Doctors
    doctors_data = [
        {'username': 'dr_ahmed', 'first_name': 'أحمد', 'last_name': 'محمود'},
        {'username': 'dr_sara', 'first_name': 'سارة', 'last_name': 'علي'},
        {'username': 'dr_khaled', 'first_name': 'خالد', 'last_name': 'حسن'},
    ]
    
    doctors = []
    for doc_data in doctors_data:
        user, created = User.objects.get_or_create(
            username=doc_data['username'],
            defaults={
                'first_name': doc_data['first_name'],
                'last_name': doc_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'doctor'}
        )
        doctors.append(user)
        print(f"  Created doctor: {user.username}")
    
    # Create Subjects
    subjects_data = [
        {'name': 'الرياضيات', 'description': 'مادة الرياضيات', 'doctor': doctors[0]},
        {'name': 'الفيزياء', 'description': 'مادة الفيزياء', 'doctor': doctors[1]},
        {'name': 'الكيمياء', 'description': 'مادة الكيمياء', 'doctor': doctors[2]},
        {'name': 'البرمجة', 'description': 'مادة البرمجة', 'doctor': doctors[0]},
    ]
    
    subjects = []
    for subj_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=subj_data['name'],
            defaults={
                'description': subj_data['description'],
                'doctor': subj_data['doctor']
            }
        )
        subjects.append(subject)
        print(f"  Created subject: {subject.name}")
    
    # Create Students
    students_data = [
        {'username': 'student1', 'first_name': 'علي', 'last_name': 'حسن'},
        {'username': 'student2', 'first_name': 'فاطمة', 'last_name': 'أحمد'},
        {'username': 'student3', 'first_name': 'محمد', 'last_name': 'خالد'},
    ]
    
    students = []
    for stud_data in students_data:
        user, created = User.objects.get_or_create(
            username=stud_data['username'],
            defaults={
                'first_name': stud_data['first_name'],
                'last_name': stud_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'student'}
        )
        students.append(user)
        print(f"  Created student: {user.username}")
    
    # Enroll Students
    for student in students:
        for subject in subjects[:3]:  # Enroll in first 3 subjects
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                subject=subject
            )
            if created:
                print(f"  Enrolled {student.username} in {subject.name}")
    
    print("\nSample data created successfully!")
    print("\nLogin credentials:")
    print("  Doctors: dr_ahmed, dr_sara, dr_khaled")
    print("  Students: student1, student2, student3")
    print("  Password for all: password123")

if __name__ == '__main__':
    create_sample_data()
```

Run it:
```bash
python mysite/create_sample_data.py
```

---

## 🔍 Verification

### Check Database:

```bash
python manage.py shell
```

```python
from myapp.models import Profile, Subject, Enrollment, Submission

print(f"Profiles: {Profile.objects.count()}")
print(f"Subjects: {Subject.objects.count()}")
print(f"Enrollments: {Enrollment.objects.count()}")
print(f"Submissions: {Submission.objects.count()}")

# List all subjects with doctors
for subject in Subject.objects.all():
    print(f"{subject.name} - Dr. {subject.doctor.username if subject.doctor else 'None'}")

# List all enrollments
for enrollment in Enrollment.objects.all():
    print(f"{enrollment.student.username} enrolled in {enrollment.subject.name}")
```

---

## 🎯 Quick Start Commands

```bash
# 1. Create migrations
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Create sample data
python mysite/create_sample_data.py

# 5. Run server
python manage.py runserver

# 6. Access application
# Student: http://127.0.0.1:8000/ (login as student1)
# Doctor: http://127.0.0.1:8000/ (login as dr_ahmed)
# Admin: http://127.0.0.1:8000/admin/
```

---

## 📝 Default Test Accounts

After running sample data script:

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Admin | admin | (your choice) | Full access |
| Doctor | dr_ahmed | password123 | Math, Programming |
| Doctor | dr_sara | password123 | Physics |
| Doctor | dr_khaled | password123 | Chemistry |
| Student | student1 | password123 | 3 subjects |
| Student | student2 | password123 | 3 subjects |
| Student | student3 | password123 | 3 subjects |

---

## 🐛 Troubleshooting

### Issue: "No such table" error

**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### Issue: Static files not loading

**Solution:**
```bash
python manage.py collectstatic
```

### Issue: Permission denied on media folder

**Solution:**
```bash
# Windows
icacls media /grant Everyone:F

# Linux/Mac
chmod -R 755 media
```

### Issue: Can't login

**Solution:**
- Verify user exists in admin panel
- Check Profile exists for user
- Reset password via admin panel

---

## ✅ Setup Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Migrations created and applied
- [ ] Superuser created
- [ ] Media directory created
- [ ] Sample data created
- [ ] Server running
- [ ] Can access admin panel
- [ ] Can login as student
- [ ] Can login as doctor
- [ ] Can upload files
- [ ] Can view submissions

---

*Last Updated: January 22, 2026*
*Version: 2.0*
