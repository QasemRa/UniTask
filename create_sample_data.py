import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import Profile, Subject, Enrollment

def create_sample_data():
    """Create sample data for testing the university system"""
    
    print("=" * 60)
    print("CREATING SAMPLE DATA FOR UNIVERSITY SYSTEM")
    print("=" * 60)
    
    print("\n📚 Creating Doctors...")
    doctors_data = [
        {'username': 'dr_ahmed', 'first_name': 'أحمد', 'last_name': 'محمود', 'email': 'ahmed@university.edu'},
        {'username': 'dr_sara', 'first_name': 'سارة', 'last_name': 'علي', 'email': 'sara@university.edu'},
        {'username': 'dr_khaled', 'first_name': 'خالد', 'last_name': 'حسن', 'email': 'khaled@university.edu'},
    ]
    
    doctors = []
    for doc_data in doctors_data:
        user, created = User.objects.get_or_create(
            username=doc_data['username'],
            defaults={
                'first_name': doc_data['first_name'],
                'last_name': doc_data['last_name'],
                'email': doc_data['email']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  ✓ Created doctor: {user.username} ({user.get_full_name()})")
        else:
            print(f"  ℹ Doctor already exists: {user.username}")
        
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'doctor'}
        )
        if profile_created:
            print(f"    ✓ Created profile for {user.username}")
        
        doctors.append(user)
    
    print("\n📖 Creating Subjects...")
    subjects_data = [
        {
            'name': 'الرياضيات',
            'description': 'مادة الرياضيات - الجبر والهندسة التحليلية',
            'doctor': doctors[0]
        },
        {
            'name': 'الفيزياء',
            'description': 'مادة الفيزياء - الميكانيكا والكهرباء',
            'doctor': doctors[1]
        },
        {
            'name': 'الكيمياء',
            'description': 'مادة الكيمياء - الكيمياء العضوية وغير العضوية',
            'doctor': doctors[2]
        },
        {
            'name': 'البرمجة',
            'description': 'مادة البرمجة - أساسيات البرمجة بلغة Python',
            'doctor': doctors[0]
        },
        {
            'name': 'قواعد البيانات',
            'description': 'مادة قواعد البيانات - SQL وتصميم قواعد البيانات',
            'doctor': doctors[1]
        },
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
        if created:
            doctor_name = subject.doctor.get_full_name() if subject.doctor else 'غير محدد'
            print(f"  ✓ Created subject: {subject.name} - Dr. {doctor_name}")
        else:
            print(f"  ℹ Subject already exists: {subject.name}")
        
        subjects.append(subject)
    
    # Create Students
    print("\n👨‍🎓 Creating Students...")
    students_data = [
        {'username': 'student1', 'first_name': 'علي', 'last_name': 'حسن', 'email': 'ali@student.edu'},
        {'username': 'student2', 'first_name': 'فاطمة', 'last_name': 'أحمد', 'email': 'fatima@student.edu'},
        {'username': 'student3', 'first_name': 'محمد', 'last_name': 'خالد', 'email': 'mohamed@student.edu'},
        {'username': 'student4', 'first_name': 'نور', 'last_name': 'سعيد', 'email': 'noor@student.edu'},
        {'username': 'student5', 'first_name': 'أمل', 'last_name': 'عبدالله', 'email': 'amal@student.edu'},
    ]
    
    students = []
    for stud_data in students_data:
        user, created = User.objects.get_or_create(
            username=stud_data['username'],
            defaults={
                'first_name': stud_data['first_name'],
                'last_name': stud_data['last_name'],
                'email': stud_data['email']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"  ✓ Created student: {user.username} ({user.get_full_name()})")
        else:
            print(f"  ℹ Student already exists: {user.username}")
        
        profile, profile_created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'student'}
        )
        if profile_created:
            print(f"    ✓ Created profile for {user.username}")
        
        students.append(user)
    
    print("\n📝 Enrolling Students in Subjects...")
    enrollment_count = 0
    
    for i, student in enumerate(students[:3]):
        for subject in subjects[:3]:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                subject=subject
            )
            if created:
                print(f"  ✓ Enrolled {student.username} in {subject.name}")
                enrollment_count += 1
            else:
                print(f"  ℹ {student.username} already enrolled in {subject.name}")
    
    for student in students[3:]:
        for subject in subjects:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                subject=subject
            )
            if created:
                print(f"  ✓ Enrolled {student.username} in {subject.name}")
                enrollment_count += 1
            else:
                print(f"  ℹ {student.username} already enrolled in {subject.name}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Doctors created: {len(doctors)}")
    print(f"✓ Subjects created: {len(subjects)}")
    print(f"✓ Students created: {len(students)}")
    print(f"✓ New enrollments: {enrollment_count}")
    print(f"✓ Total enrollments: {Enrollment.objects.count()}")
    
    print("\n" + "=" * 60)
    print("LOGIN CREDENTIALS")
    print("=" * 60)
    print("\n📚 Doctors:")
    for doctor in doctors:
        subjects_taught = Subject.objects.filter(doctor=doctor)
        print(f"  Username: {doctor.username}")
        print(f"  Password: password123")
        print(f"  Subjects: {', '.join([s.name for s in subjects_taught])}")
        print()
    
    print("👨‍🎓 Students:")
    for student in students:
        enrolled_subjects = Enrollment.objects.filter(student=student).count()
        print(f"  Username: {student.username}")
        print(f"  Password: password123")
        print(f"  Enrolled in: {enrolled_subjects} subjects")
        print()
    
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Run the server: python manage.py runserver")
    print("2. Access the application: http://127.0.0.1:8000/")
    print("3. Login with any of the credentials above")
    print("4. Test uploading assignments as a student")
    print("5. Test viewing submissions as a doctor")
    print("=" * 60)

if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you have run migrations first:")
        print("  python manage.py makemigrations")
        print("  python manage.py migrate")
