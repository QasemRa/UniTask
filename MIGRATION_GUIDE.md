# 🔄 Database Migration Guide

## Overview
This guide explains how to migrate from the old database structure to the new admin-controlled subject assignment system.

---

## Changes Made

### Old Structure:
- Profile model had a `subject` field for doctors
- Submission model had a `subject` CharField
- No enrollment tracking
- No subject-doctor relationship

### New Structure:
- **Subject Model**: Separate table for subjects with assigned doctors
- **Enrollment Model**: Links students to subjects
- **Updated Submission**: Uses ForeignKey to Subject instead of CharField
- **Removed**: `subject` field from Profile model

---

## Migration Steps

### Step 1: Create Migration Files

```bash
cd mysite
python manage.py makemigrations
```

This will create migration files for the new models (Subject, Enrollment) and changes to existing models.

### Step 2: Review Migration Files

Check the generated migration files in `mysite/myapp/migrations/` to ensure they look correct.

### Step 3: Backup Your Database (IMPORTANT!)

```bash
# For SQLite
cp db.sqlite3 db.sqlite3.backup

# For PostgreSQL
pg_dump your_database > backup.sql

# For MySQL
mysqldump -u username -p database_name > backup.sql
```

### Step 4: Run Migrations

```bash
python manage.py migrate
```

---

## Data Migration Script

If you have existing data, you'll need to migrate it to the new structure. Here's a Python script to help:

### Create: `mysite/migrate_data.py`

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import Profile, Subject, Enrollment, Submission

def migrate_subjects_from_profiles():
    """Create Subject objects from doctor profiles"""
    print("Migrating subjects from doctor profiles...")
    
    doctors = Profile.objects.filter(role='doctor', subject__isnull=False)
    created_subjects = {}
    
    for doctor_profile in doctors:
        subject_name = doctor_profile.subject
        
        if subject_name and subject_name not in created_subjects:
            subject, created = Subject.objects.get_or_create(
                name=subject_name,
                defaults={'doctor': doctor_profile.user}
            )
            created_subjects[subject_name] = subject
            print(f"  {'Created' if created else 'Found'} subject: {subject_name}")
    
    print(f"Total subjects: {len(created_subjects)}")
    return created_subjects

def migrate_submissions():
    """Update old submissions to use Subject ForeignKey"""
    print("\nMigrating submissions...")
    
    # Note: This assumes you've already run makemigrations and migrate
    # The old 'subject' CharField should now be a ForeignKey
    
    # If you have old data, you'll need to handle it manually
    # This is just a template
    
    print("Submissions migration complete")

def create_sample_enrollments():
    """Create sample enrollments for testing"""
    print("\nCreating sample enrollments...")
    
    students = User.objects.filter(profile__role='student')
    subjects = Subject.objects.all()
    
    if not subjects.exists():
        print("  No subjects found. Please create subjects first.")
        return
    
    for student in students:
        # Enroll each student in all subjects (you can customize this)
        for subject in subjects:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                subject=subject
            )
            if created:
                print(f"  Enrolled {student.username} in {subject.name}")
    
    print("Sample enrollments created")

if __name__ == '__main__':
    print("=" * 50)
    print("DATA MIGRATION SCRIPT")
    print("=" * 50)
    
    migrate_subjects_from_profiles()
    migrate_submissions()
    create_sample_enrollments()
    
    print("\n" + "=" * 50)
    print("MIGRATION COMPLETE!")
    print("=" * 50)
```

### Run the migration script:

```bash
python mysite/migrate_data.py
```

---

## Manual Setup (Fresh Installation)

If you're starting fresh or prefer manual setup:

### 1. Create Subjects via Admin Panel

1. Login to admin: http://127.0.0.1:8000/admin/
2. Go to "Subjects"
3. Click "Add Subject"
4. Fill in:
   - Name: e.g., "Mathematics"
   - Description: (optional)
   - Doctor: Select a doctor user
5. Save

### 2. Enroll Students

1. Go to "Enrollments"
2. Click "Add Enrollment"
3. Select:
   - Student: Choose a student
   - Subject: Choose a subject
4. Save

### 3. Test the System

1. Login as a student
2. You should see only enrolled subjects
3. Upload an assignment
4. Login as the assigned doctor
5. You should see the submission

---

## Troubleshooting

### Issue: Migration conflicts

**Solution:**
```bash
python manage.py migrate --fake-initial
```

### Issue: Old data not showing

**Solution:**
- Check if Subject objects exist
- Check if Enrollments exist
- Verify doctor assignments in Subject model

### Issue: Students can't see subjects

**Solution:**
- Ensure students are enrolled via Enrollment model
- Check that subjects have assigned doctors

### Issue: Doctors can't see submissions

**Solution:**
- Verify doctor is assigned to the subject
- Check that submissions reference the correct Subject

---

## Verification Checklist

After migration, verify:

- [ ] All subjects are created in Subject model
- [ ] Each subject has an assigned doctor
- [ ] Students are enrolled in appropriate subjects
- [ ] Old submissions are linked to new Subject objects
- [ ] Student dashboard shows only enrolled subjects
- [ ] Doctor dashboard shows only assigned subjects
- [ ] File uploads work correctly
- [ ] Plagiarism detection works

---

## Rollback Plan

If something goes wrong:

### 1. Restore Database Backup

```bash
# For SQLite
cp db.sqlite3.backup db.sqlite3

# For PostgreSQL
psql your_database < backup.sql

# For MySQL
mysql -u username -p database_name < backup.sql
```

### 2. Revert Code Changes

```bash
git checkout previous_commit_hash
```

### 3. Run Old Migrations

```bash
python manage.py migrate myapp previous_migration_number
```

---

## Post-Migration Tasks

### 1. Update Admin Users

Ensure all admin users have proper permissions:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from myapp.models import Profile

# Create profiles for users without them
for user in User.objects.all():
    if not hasattr(user, 'profile'):
        role = 'doctor' if user.is_staff else 'student'
        Profile.objects.create(user=user, role=role)
        print(f"Created profile for {user.username}")
```

### 2. Clean Up Old Data

Remove the old `subject` field from Profile model after confirming everything works:

```python
# In models.py, the field is already removed
# Just ensure migrations are complete
```

### 3. Update Documentation

- Update user guides
- Update API documentation (if any)
- Update training materials

---

## Testing After Migration

### Test Student Workflow:
1. Login as student
2. Check enrolled subjects display
3. Upload assignment to each subject
4. Verify file appears in submissions
5. Check doctor name shows correctly

### Test Doctor Workflow:
1. Login as doctor
2. Check assigned subjects display
3. Verify submissions from students
4. Check plagiarism detection
5. Download student files

### Test Admin Workflow:
1. Login to admin panel
2. Create new subject
3. Assign doctor to subject
4. Enroll student in subject
5. Verify changes reflect in dashboards

---

## Support

If you encounter issues:

1. Check Django logs
2. Check browser console for errors
3. Verify database integrity
4. Review migration files
5. Contact system administrator

---

*Last Updated: January 22, 2026*
*Version: 2.0*
