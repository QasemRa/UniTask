from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UploadForm, PDFCompareForm
from .models import Submission, Profile, Enrollment, Subject
from .utils import extract_text_from_pdf, compute_similarity
from django.conf import settings
import os
import tempfile

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        user = self.request.user
        try:
            profile = user.profile
            if profile.role == 'student':
                return '/student/'
            elif profile.role == 'doctor':
                return '/doctor/'
            elif profile.role == 'admin':
                return '/admin/'
        except Profile.DoesNotExist:
            messages.error(self.request, 'الملف الشخصي غير موجود. يرجى الاتصال بالإدارة.')
            return '/'
        return '/'


@method_decorator(login_required, name='dispatch')
class StudentDashboardView(View):
    """Main dashboard view with statistics"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('subject').order_by('-upload_date')
        
        subjects_data = []
        for enrollment in enrollments:
            subject = enrollment.subject
            subject_submissions = submissions.filter(subject=subject)
            
            subjects_data.append({
                'subject': subject,
                'doctor': subject.doctor,
                'total_submissions': subject_submissions.count(),
                'submissions': subject_submissions
            })
        
        context = {
            'subjects_data': subjects_data,
            'total_subjects': enrollments.count(),
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/student_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class StudentUploadView(View):
    """Upload assignment page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        form = UploadForm(user=request.user)
        
        context = {
            'form': form,
            'enrollments': enrollments,
        }
        
        return render(request, 'myapp/student_upload.html', context)

    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        form = UploadForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            subject = form.cleaned_data['subject']
            is_enrolled = Enrollment.objects.filter(
                student=request.user,
                subject=subject
            ).exists()
            
            if not is_enrolled:
                messages.error(request, 'أنت غير مسجل في هذه المادة.')
                return redirect('/student/upload/')
            
            submission = form.save(commit=False)
            submission.student = request.user
            submission.save()
            
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, submission.file.name)
                submission.text = extract_text_from_pdf(file_path)
                submission.save()
            except Exception as e:
                messages.warning(request, f'تم رفع الملف بنجاح، لكن فشل استخراج النص: {str(e)}')
            
            messages.success(request, f'تم رفع الواجب بنجاح لمادة {subject.name}!')
            return redirect('/student/upload/')
        
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        context = {
            'form': form,
            'enrollments': enrollments,
        }
        
        return render(request, 'myapp/student_upload.html', context)


@method_decorator(login_required, name='dispatch')
class StudentSubjectsView(View):
    """Enrolled subjects page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('subject').order_by('-upload_date')
        
        subjects_data = []
        for enrollment in enrollments:
            subject = enrollment.subject
            subject_submissions = submissions.filter(subject=subject)
            
            subjects_data.append({
                'subject': subject,
                'doctor': subject.doctor,
                'total_submissions': subject_submissions.count(),
                'submissions': subject_submissions
            })
        
        context = {
            'subjects_data': subjects_data,
            'enrollments': enrollments,
            'total_subjects': enrollments.count(),
        }
        
        return render(request, 'myapp/student_subjects.html', context)


@method_decorator(login_required, name='dispatch')
class StudentSubmissionsView(View):
    """My submissions page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'student':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        enrollments = Enrollment.objects.filter(
            student=request.user
        ).select_related('subject', 'subject__doctor')
        
        submissions = Submission.objects.filter(
            student=request.user
        ).select_related('subject').order_by('-upload_date')
        
        context = {
            'submissions': submissions,
            'enrollments': enrollments,
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/student_submissions.html', context)


@method_decorator(login_required, name='dispatch')
class StudentView(View):
    def get(self, request):
        return redirect('/student/')

    def post(self, request):
        return redirect('/student/')


@method_decorator(login_required, name='dispatch')
class DoctorView(View):
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        subjects = Subject.objects.filter(doctor=request.user)
        
        if subjects.count() == 1:

            return redirect(f'/doctor/subject/{subjects.first().id}/')
        else:

            return redirect('/doctor/select-subject/')

    def post(self, request):
        return self.get(request)


@method_decorator(login_required, name='dispatch')
class DoctorDashboardView(View):
    """Main doctor dashboard with statistics"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        assigned_subjects = Subject.objects.filter(
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions')
        
        submissions = Submission.objects.filter(
            subject__doctor=request.user
        ).select_related('student', 'subject').order_by('-upload_date')
        
        subjects_data = []
        all_texts = []
        all_submissions_list = []
        
        for subject in assigned_subjects:
            subject_submissions = submissions.filter(subject=subject)
            enrolled_count = subject.enrollments.count()
            
            subjects_data.append({
                'subject': subject,
                'submissions_count': subject_submissions.count(),
                'enrolled_count': enrolled_count,
                'submissions': subject_submissions
            })
            
            for sub in subject_submissions:
                if sub.text:
                    all_texts.append(sub.text)
                    all_submissions_list.append(sub)
        
        similarities = []
        if len(all_texts) >= 2:
            try:
                similarities = compute_similarity(all_texts)
                for sim in similarities:
                    if sim['text1_index'] < len(all_submissions_list) and sim['text2_index'] < len(all_submissions_list):
                        sim['student_a'] = all_submissions_list[sim['text1_index']].student.username
                        sim['student_b'] = all_submissions_list[sim['text2_index']].student.username
                        sim['subject'] = all_submissions_list[sim['text1_index']].subject.name
            except Exception as e:
                messages.warning(request, f'فشل حساب التشابه: {str(e)}')
        
        high_similarity_count = sum(1 for sim in similarities if sim.get('similarity', 0) > 70)
        unique_students = submissions.values('student').distinct().count()
        
        context = {
            'assigned_subjects': assigned_subjects,
            'subjects_data': subjects_data,
            'submissions': submissions,
            'similarities': similarities,
            'total_subjects': assigned_subjects.count(),
            'total_submissions': submissions.count(),
            'unique_students': unique_students,
            'high_similarity_count': high_similarity_count
        }
        
        return render(request, 'myapp/doctor_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectsView(View):
    """Doctor subjects page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        assigned_subjects = Subject.objects.filter(
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions')
        
        submissions = Submission.objects.filter(
            subject__doctor=request.user
        ).select_related('student', 'subject').order_by('-upload_date')
        
        subjects_data = []
        for subject in assigned_subjects:
            subject_submissions = submissions.filter(subject=subject)
            enrolled_count = subject.enrollments.count()
            
            subjects_data.append({
                'subject': subject,
                'submissions_count': subject_submissions.count(),
                'enrolled_count': enrolled_count,
                'submissions': subject_submissions
            })
        
        context = {
            'assigned_subjects': assigned_subjects,
            'subjects_data': subjects_data,
            'submissions': submissions,
            'total_subjects': assigned_subjects.count(),
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/doctor_subjects.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubmissionsView(View):
    """Doctor submissions page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        submissions = Submission.objects.filter(
            subject__doctor=request.user
        ).select_related('student', 'subject').order_by('-upload_date')
        
        context = {
            'submissions': submissions,
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/doctor_submissions.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorPlagiarismView(View):
    """Doctor plagiarism detection page only"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        assigned_subjects = Subject.objects.filter(
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions')
        
        submissions = Submission.objects.filter(
            subject__doctor=request.user
        ).select_related('student', 'subject').order_by('-upload_date')
        
        all_texts = []
        all_submissions_list = []
        
        for subject in assigned_subjects:
            subject_submissions = submissions.filter(subject=subject)
            for sub in subject_submissions:
                if sub.text:
                    all_texts.append(sub.text)
                    all_submissions_list.append(sub)
        
        similarities = []
        if len(all_texts) >= 2:
            try:
                similarities = compute_similarity(all_texts)
                for sim in similarities:
                    if sim['text1_index'] < len(all_submissions_list) and sim['text2_index'] < len(all_submissions_list):
                        sim['student_a'] = all_submissions_list[sim['text1_index']].student.username
                        sim['student_b'] = all_submissions_list[sim['text2_index']].student.username
                        sim['subject'] = all_submissions_list[sim['text1_index']].subject.name
            except Exception as e:
                messages.warning(request, f'فشل حساب التشابه: {str(e)}')
        
        high_similarity_count = sum(1 for sim in similarities if sim.get('similarity', 0) > 70)
        
        context = {
            'assigned_subjects': assigned_subjects,
            'submissions': submissions,
            'similarities': similarities,
            'total_subjects': assigned_subjects.count(),
            'total_submissions': submissions.count(),
            'high_similarity_count': high_similarity_count
        }
        
        return render(request, 'myapp/doctor_plagiarism.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectSelectView(View):
    """Select subject to manage"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        subjects = Subject.objects.filter(
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions')
        
        context = {
            'subjects': subjects,
            'total_subjects': subjects.count()
        }
        
        return render(request, 'myapp/doctor_subject_select.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectDetailView(View):
    """Manage specific subject"""
    def get(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id, doctor=request.user)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة أو غير مسندة إليك.')
            return redirect('doctor_subject_select')
        
        subject = Subject.objects.filter(
            id=subject_id,
            doctor=request.user
        ).prefetch_related('enrollments', 'submissions').first()
        
        context = {
            'subject': subject,
            'total_submissions': subject.submissions.count(),
            'total_students': subject.enrollments.count()
        }
        
        return render(request, 'myapp/doctor_subject_detail.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectSubmissionsView(View):
    """View submissions for specific subject"""
    def get(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id, doctor=request.user)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة أو غير مسندة إليك.')
            return redirect('doctor_subject_select')
        
        submissions = Submission.objects.filter(
            subject=subject
        ).select_related('student').order_by('-upload_date')
        
        context = {
            'subject': subject,
            'submissions': submissions,
            'total_submissions': submissions.count()
        }
        
        return render(request, 'myapp/doctor_subject_submissions.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectPlagiarismView(View):
    """View plagiarism detection for specific subject"""
    def get(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id, doctor=request.user)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة أو غير مسندة إليك.')
            return redirect('doctor_subject_select')
        
        submissions = Submission.objects.filter(
            subject=subject
        ).select_related('student').order_by('-upload_date')
        
        all_texts = []
        all_submissions_list = []
        
        for sub in submissions:
            if sub.text:
                all_texts.append(sub.text)
                all_submissions_list.append(sub)
        
        similarities = []
        if len(all_texts) >= 2:
            try:
                similarities = compute_similarity(all_texts)
                for sim in similarities:
                    if sim['text1_index'] < len(all_submissions_list) and sim['text2_index'] < len(all_submissions_list):
                        sim['student_a'] = all_submissions_list[sim['text1_index']].student.username
                        sim['student_b'] = all_submissions_list[sim['text2_index']].student.username
            except Exception as e:
                messages.warning(request, f'فشل حساب التشابه: {str(e)}')
        
        high_similarity_count = sum(1 for sim in similarities if sim.get('similarity', 0) > 70)
        
        context = {
            'subject': subject,
            'submissions': submissions,
            'similarities': similarities,
            'total_submissions': submissions.count(),
            'high_similarity_count': high_similarity_count
        }
        
        return render(request, 'myapp/doctor_subject_plagiarism.html', context)


@method_decorator(login_required, name='dispatch')
class DoctorSubjectStudentsView(View):
    """Manage students for specific subject"""
    def get(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id, doctor=request.user)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة أو غير مسندة إليك.')
            return redirect('doctor_subject_select')
        
        enrolled_students = Enrollment.objects.filter(
            subject=subject
        ).select_related('student').order_by('-enrolled_date')
        

        enrolled_student_ids = enrolled_students.values_list('student_id', flat=True)
        available_students = User.objects.filter(
            profile__role='student'
        ).exclude(id__in=enrolled_student_ids)
        
        context = {
            'subject': subject,
            'enrolled_students': enrolled_students,
            'available_students': available_students,
            'total_students': enrolled_students.count()
        }
        
        return render(request, 'myapp/doctor_subject_students.html', context)
    
    def post(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id, doctor=request.user)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة أو غير مسندة إليك.')
            return redirect('doctor_subject_select')
        
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        
        if action == 'add' and student_id:
            try:
                student = User.objects.get(id=student_id, profile__role='student')
                Enrollment.objects.get_or_create(
                    student=student,
                    subject=subject
                )
                student_name = student.get_full_name if student.get_full_name() else student.username
                messages.success(request, f'تم إضافة الطالب {student_name} بنجاح.')
            except User.DoesNotExist:
                messages.error(request, 'الطالب غير موجود.')
        
        elif action == 'remove' and student_id:
            try:
                student = User.objects.get(id=student_id, profile__role='student')
                enrollment = Enrollment.objects.get(student=student, subject=subject)
                enrollment.delete()
                student_name = student.get_full_name if student.get_full_name() else student.username
                messages.success(request, f'تم إزالة الطالب {student_name} بنجاح.')
            except (User.DoesNotExist, Enrollment.DoesNotExist):
                messages.error(request, 'فشل إزالة الطالب.')
        
        return redirect('doctor_subject_students', subject_id=subject_id)


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    """Admin dashboard with system statistics"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        total_doctors = User.objects.filter(profile__role='doctor').count()
        total_students = User.objects.filter(profile__role='student').count()
        total_subjects = Subject.objects.count()
        total_submissions = Submission.objects.count()
        
        context = {
            'total_doctors': total_doctors,
            'total_students': total_students,
            'total_subjects': total_subjects,
            'total_submissions': total_submissions
        }
        
        return render(request, 'admin_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class AdminAddDoctorView(View):
    """Add new doctor account"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        return render(request, 'admin_add_doctor.html')
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم بالفعل.')
            return redirect('admin_add_doctor')
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            Profile.objects.create(
                user=user,
                role='doctor',
                phone=phone,
                department=department
            )
            
            messages.success(request, f'تم إضافة الدكتور {first_name} {last_name} بنجاح.')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'فشل إضافة الدكتور: {str(e)}')
            return redirect('admin_add_doctor')


@method_decorator(login_required, name='dispatch')
class AdminAddStudentView(View):
    """Add new student account"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        return render(request, 'admin_add_student.html')
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        student_id = request.POST.get('student_id')
        department = request.POST.get('department')
        study_level = request.POST.get('study_level')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'البريد الإلكتروني مستخدم بالفعل.')
            return redirect('admin_add_student')
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            Profile.objects.create(
                user=user,
                role='student',
                phone=phone,
                student_id=student_id,
                department=department,
                study_level=study_level
            )
            
            messages.success(request, f'تم إضافة الطالب {first_name} {last_name} بنجاح.')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'فشل إضافة الطالب: {str(e)}')
            return redirect('admin_add_student')


@method_decorator(login_required, name='dispatch')
class AdminAssignSubjectsView(View):
    """Manage subjects and assign doctors"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        subjects = Subject.objects.all().prefetch_related('enrollments', 'doctor')
        doctors = User.objects.filter(profile__role='doctor', profile__is_active=True)
        
        context = {
            'subjects': subjects,
            'doctors': doctors
        }
        
        return render(request, 'admin_assign_subjects.html', context)
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        action = request.POST.get('action')
        
        if action == 'add_subject':
            subject_name = request.POST.get('subject_name')
            subject_description = request.POST.get('subject_description')
            doctor_id = request.POST.get('doctor_id')
            
            try:
                doctor = User.objects.get(id=doctor_id, profile__role='doctor')
                subject = Subject.objects.create(
                    name=subject_name,
                    description=subject_description,
                    doctor=doctor
                )
                messages.success(request, f'تم إضافة المادة {subject_name} بنجاح.')
            except Exception as e:
                messages.error(request, f'فشل إضافة المادة: {str(e)}')
        
        elif action == 'assign_doctor':
            subject_id = request.POST.get('subject_id')
            new_doctor_id = request.POST.get('new_doctor_id')
            
            try:
                subject = Subject.objects.get(id=subject_id)
                if new_doctor_id:
                    new_doctor = User.objects.get(id=new_doctor_id, profile__role='doctor')
                    subject.doctor = new_doctor
                    messages.success(request, f'تم تحديد الدكتور للمادة {subject.name} بنجاح.')
                else:
                    subject.doctor = None
                    messages.success(request, f'تم إلغاء تحديد الدكتور للمادة {subject.name}.')
                subject.save()
            except Exception as e:
                messages.error(request, f'فشل تحديث المادة: {str(e)}')
        
        return redirect('admin_assign_subjects')


@method_decorator(login_required, name='dispatch')
class AdminManageUsersView(View):
    """Manage users (activate/deactivate)"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        doctors = User.objects.filter(profile__role='doctor').prefetch_related('teaching_subjects')
        students = User.objects.filter(profile__role='student').prefetch_related('enrollments', 'submissions')
        
        context = {
            'doctors': doctors,
            'students': students
        }
        
        return render(request, 'admin_manage_users.html', context)
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            
            if action == 'toggle_doctor' and profile.role == 'doctor':
                profile.is_active = not profile.is_active
                profile.save()
                status = 'تفعيل' if profile.is_active else 'تعطيل'
                messages.success(request, f'تم {status} حساب الدكتور {user.get_full_name()}.')
            
            elif action == 'toggle_student' and profile.role == 'student':
                profile.is_active = not profile.is_active
                profile.save()
                status = 'تفعيل' if profile.is_active else 'تعطيل'
                messages.success(request, f'تم {status} حساب الطالب {user.get_full_name()}.')
                
        except Exception as e:
            messages.error(request, f'فشل تحديث الحساب: {str(e)}')
        
        return redirect('admin_manage_users')


@method_decorator(login_required, name='dispatch')
class AdminEnrollStudentsView(View):
    """Manage student enrollment in subjects"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        students = User.objects.filter(profile__role='student', profile__is_active=True)
        subjects = Subject.objects.all().prefetch_related('enrollments', 'doctor')
        

        unenrolled_students = []
        for student in students:
            if student.enrollments.count() == 0:
                unenrolled_students.append(student)
        
        context = {
            'students': students,
            'subjects': subjects,
            'unenrolled_students': unenrolled_students
        }
        
        return render(request, 'admin_enroll_students.html', context)
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')
        
        if action == 'enroll' and student_id and subject_id:
            try:
                student = User.objects.get(id=student_id, profile__role='student')
                subject = Subject.objects.get(id=subject_id)
                
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    subject=subject
                )
                
                if created:
                    messages.success(request, f'تم تسجيل الطالب {student.get_full_name() if student.get_full_name() else student.username} في مادة {subject.name} بنجاح.')
                else:
                    messages.warning(request, f'الطالب {student.get_full_name() if student.get_full_name() else student.username} مسجل بالفعل في مادة {subject.name}.')
                    
            except (User.DoesNotExist, Subject.DoesNotExist):
                messages.error(request, 'فشل التسجيل. الطالب أو المادة غير موجودة.')
        
        return redirect('admin_enroll_students')


@method_decorator(login_required, name='dispatch')
class AdminSubjectStudentsView(View):
    """Manage students for specific subject (admin version)"""
    def get(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة.')
            return redirect('admin_enroll_students')
        
        enrolled_students = Enrollment.objects.filter(
            subject=subject
        ).select_related('student').order_by('-enrolled_date')
        

        enrolled_student_ids = enrolled_students.values_list('student_id', flat=True)
        available_students = User.objects.filter(
            profile__role='student',
            profile__is_active=True
        ).exclude(id__in=enrolled_student_ids)
        
        context = {
            'subject': subject,
            'enrolled_students': enrolled_students,
            'available_students': available_students,
            'total_students': enrolled_students.count()
        }
        
        return render(request, 'admin_subject_students.html', context)
    
    def post(self, request, subject_id):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, 'المادة غير موجودة.')
            return redirect('admin_enroll_students')
        
        action = request.POST.get('action')
        student_id = request.POST.get('student_id')
        
        if action == 'add' and student_id:
            try:
                student = User.objects.get(id=student_id, profile__role='student')
                Enrollment.objects.get_or_create(
                    student=student,
                    subject=subject
                )
                student_name = student.get_full_name if student.get_full_name() else student.username
                messages.success(request, f'تم إضافة الطالب {student_name} بنجاح.')
            except User.DoesNotExist:
                messages.error(request, 'الطالب غير موجود.')
        
        elif action == 'remove' and student_id:
            try:
                student = User.objects.get(id=student_id, profile__role='student')
                enrollment = Enrollment.objects.get(student=student, subject=subject)
                enrollment.delete()
                student_name = student.get_full_name if student.get_full_name() else student.username
                messages.success(request, f'تم إزالة الطالب {student_name} بنجاح.')
            except (User.DoesNotExist, Enrollment.DoesNotExist):
                messages.error(request, 'فشل إزالة الطالب.')
        
        return redirect('admin_subject_students', subject_id=subject_id)


@method_decorator(login_required, name='dispatch')
class PDFCompareView(View):
    """Dedicated PDF comparison view for handwritten text similarity detection"""
    def get(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        form = PDFCompareForm()
        context = {
            'form': form,
        }
        return render(request, 'myapp/pdf_compare.html', context)
    
    def post(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'doctor':
            messages.error(request, 'غير مصرح لك بالوصول إلى هذه الصفحة.')
            return redirect('/')
        
        form = PDFCompareForm(request.POST, request.FILES)
        
        if form.is_valid():
            files = form.cleaned_data['pdf_files']
            file_names = []
            extracted_texts = []
            temp_files = []
            
            try:

                for file in files:
                    file_names.append(file.name)
                    

                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                        for chunk in file.chunks():
                            temp_file.write(chunk)
                        temp_files.append(temp_file.name)
                

                for temp_file_path in temp_files:
                    text = extract_text_from_pdf(temp_file_path)
                    extracted_texts.append(text)
                

                similarities = compute_similarity(extracted_texts)
                

                for sim in similarities:
                    sim['file1_name'] = file_names[sim['text1_index']]
                    sim['file2_name'] = file_names[sim['text2_index']]
                

                for temp_file_path in temp_files:
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                
                context = {
                    'form': form,
                    'file_names': file_names,
                    'extracted_texts': extracted_texts,
                    'similarities': similarities,
                    'total_files': len(files),
                    'high_similarity_count': sum(1 for sim in similarities if sim.get('similarity', 0) > 70)
                }
                
                return render(request, 'myapp/pdf_compare.html', context)
                
            except Exception as e:

                for temp_file_path in temp_files:
                    try:
                        os.unlink(temp_file_path)
                    except:
                        pass
                
                messages.error(request, f'حدث خطأ أثناء معالجة الملفات: {str(e)}')
        
        context = {
            'form': form,
        }
        return render(request, 'myapp/pdf_compare.html', context)
